"""
支持以下attrs-inspector:
* attr可以使用动态参数，传入VSO xxx VEO来指定动态参数
* 可以被ifbr语句控制

Type(X)  ;# 允许指定基础类型
    X can be one of the following types:
    - int   (QSpinBox)
    - float (QDoubleSpinBox)
    - str   (QLineEdit)
    - bool  (QCheckBox)
    - class (等效于Serialize)
Range(X[, Y[, S) ;# 允许指定范围
    - X: 当只有一个参数时，表示最大值；否则表示最小值
    - Y: 最大值
    - S: 步长 必须>0
    * 这实质上会创建一个python range对象，所以范围的取值是左闭右开的 [X, Y)
    * 当描述符与Type(int)结合时，提升QSpinBox为QSlider，且步长默认值为1
    * 当描述符与Type(float)结合时，提升QDoubleSpinBox为QSlider，且步长默认值为0.01
    * 当描述符与Type(int|float)结合并且S的类型不匹配时，会抛出异常
    * 当描述符与Type(str|bool)结合时，会抛出异常
Enum(X, Y, Z, ...) ;# 强制要求输入必须为枚举值
    * X, Y, Z, ...: 枚举值
    * 当描述符与Type(int|float|str)结合时，提升QXXX为QComboBox
    * QComboBox和QSlider互相冲突，最终会以QComboBox为准
    * 当描述符与Type(bool)结合时，会抛出异常
Color(fg[, bg) ;# 设置整个控件的全局前景色和全局背景色
    * fg: 前景色
    * bg: 背景色
    * 支持 #RRGGBB, rgb(r, g, b) 格式
Tooltip(X) ;# 设置控件的提示信息
Label(X) ;# 设置别名标签
    * 如果没有设置别名标签，会使用变量名作为标签的文本
Serialize ;# 序列化
    * 目标对象属性类型必须为int|float|str|bool中的一种
    * None会被解释为str类型的""
    * 忽略startswith('_')的属性
Group([X) ;# 接下来的控件会被分组到Group:X中
    * X: 分组的标题
    * 当没有指定X时，接下来的控件会重新回到上一级分组
    * 一个Group是可以被折叠起来的
Header(X) ;# 在此处插入一个标题，例如 X:
Readonly() ;# 当数据被该描述符描述时，数据不可编辑，只能被查看
Separator() ;# 在此处插入一个分隔符
Space([x) ;# 在此处插入一个空白控件，高度为x.
    * x: 高度
    * 当没有指定x时，高度为标准间距
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox, QLineEdit, QCheckBox, QComboBox, QPushButton, QApplication, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter, QPen, QColor, QBrush
from reft._mono_qsliders import QDoubleSlider, QIntSlider
from reft._mono_qshadows import QShadowLabel
from reft.mono import Mono, MonoAttr
from reft._rangef import rangef, find_closest
import warnings
import types
import sys
warnings.filterwarnings("ignore", category=DeprecationWarning)
BUILTIN_TYPES = (
    int, float, complex, str, bool, bytes, bytearray, memoryview,
    tuple, list, dict, set, frozenset,
    types.FunctionType, types.BuiltinFunctionType, types.MethodType,
    types.LambdaType, types.CodeType, types.ModuleType,
    types.TracebackType, types.FrameType, types.GeneratorType,
    types.CoroutineType
)


def _is_builtin_instance(inst) -> bool:
    """
    检查对象 inst 是否是 Python 的内置类型实例。

    参数:
    inst -- 要检查的对象

    返回:
    如果是内置类型实例，则返回 True，否则返回 False
    """
    # 定义一个元组，包含所有内置类型的类型

    # 检查 inst 的类型是否在这个元组中
    return isinstance(inst, BUILTIN_TYPES)

def api_merge_colors(*qc):
    # 初始化颜色累加器
    red_sum, green_sum, blue_sum, alpha_sum = 0, 0, 0, 0
    count = 0       # 权重和

    # 累加所有颜色的 RGB 和 Alpha 值
    for color in qc:
        if isinstance(color, tuple):
            weight, color = color
        else:
            weight = 1
        red_sum += color.red() * weight
        green_sum += color.green() * weight
        blue_sum += color.blue() * weight
        alpha_sum += color.alpha() * weight
        count += weight

    # 计算平均值
    if count > 0:
        red_avg = red_sum // count
        green_avg = green_sum // count
        blue_avg = blue_sum // count
        alpha_avg = alpha_sum // count
    else:
        # 如果没有传入任何颜色，返回一个默认的透明颜色
        return QColor(0, 0, 0, 0)

    # 创建并返回新的 QColor 对象
    return QColor(red_avg, green_avg, blue_avg, alpha_avg)

class FTMonoaRuntimeEvalError(Exception):
    def __init__(self, monoa, msg):
        txt = f"\n\t{str(msg)}\n\n\tLineno:{monoa.lineno}, Target:\n\t\t{monoa}"
        super().__init__(txt)

class FTQMonoWidgetRecvObjectError(Exception):
    pass

class FTMonoaRuntimeUnexpectedColor(FTMonoaRuntimeEvalError):
    pass

class FTMonoaRuntimeDismatchedEnumType(FTMonoaRuntimeEvalError):
    pass

class FTMonoaRuntimeDismatchedRangeType(FTMonoaRuntimeEvalError):
    pass


def _default_color(FG_COLOR, FG_ALPHA, BG_COLOR, BG_ALPHA) -> tuple:
    if FG_COLOR is None:
        fg = None
    else:
        fg = QColor(FG_COLOR)
        fg.setAlpha(FG_ALPHA)
    if BG_COLOR is None:
        bg = None
    else:
        bg = QColor(BG_COLOR)
        bg.setAlpha(BG_ALPHA)

    if fg is None and bg is None:
        return None
    return (fg, bg)

class MonoaRuntime:
    BG_ALPHA = 15
    BG_COLOR = "#FFFF00"
    FG_ALPHA = 200
    FG_COLOR = None
    DEFAULTS = {
        "type": None,
        "range": None,
        "enum": None,
        "serialize": False,
        "color": _default_color(FG_COLOR, FG_ALPHA, BG_COLOR, BG_ALPHA),
        "tooltip": None,
        "label": None,
        "group": None,
        "header": None,
        "readonly": False,
        "separator": False,
        "space": None
    }
    def __init__(self):
        self.monoa_env = {}
        self.monoa_env['Type'] = self.Type
        self.monoa_env['Range'] = self.Range
        self.monoa_env['Enum'] = self.Enum
        self.monoa_env['Serialize'] = self.Serialize
        self.monoa_env['Color'] = self.Color
        self.monoa_env['Tooltip'] = self.Tooltip
        self.monoa_env['Label'] = self.Label
        self.monoa_env['Group'] = self.Group
        self.monoa_env['Header'] = self.Header
        self.monoa_env['Readonly'] = self.Readonly
        self.monoa_env['Separate'] = self.Separator
        self.monoa_env['Separator'] = self.Separator
        self.monoa_env['Space'] = self.Space
        self.monoa_env['Spacer'] = self.Space
        self.cmonoa = None


    @staticmethod
    def _remove_builtins(_d) -> dict:
        return {k: v for k, v in _d.items() if not k.startswith('__')}

    def Type(self, x):
        if isinstance(x, str):
            x = x.lower()
            if x == 'int':
                return {"type": int}
            elif x == 'float':
                return {"type": float}
            elif x == 'str':
                return {"type": str}
            elif x == 'bool':
                return {"type": bool}
            elif x == 'class':
                return {"type": object}
            else:
                raise FTMonoaRuntimeEvalError(self.cmonoa, f"Type '{x}' is not supported.")
        elif x in (int, float, str, bool, object):
            return {"type": x}
        raise FTMonoaRuntimeEvalError(self.cmonoa, f"Type '{x}' is not supported.")

    def Range(self, x, y=None, s=1):
        if y is None:
            _range = rangef(0, x, s)
        else:
            # y must be greater than x
            if y <= x:
                raise FTMonoaRuntimeEvalError(self.cmonoa, f"End of range must be greater than start. but got range({x}, {y})")
            _range = rangef(x, y, s)

        # s must be greater than 0
        if s <= 0:
            raise FTMonoaRuntimeEvalError(self.cmonoa, f"Step of range must be greater than 0. but got step({s})")
        return {"range": _range}

    def Enum(self, *args):
        if not args:
            raise FTMonoaRuntimeEvalError(self.cmonoa, f"Enum must have at least one argument.")
        return {"enum": list(args)}

    def Serialize(self, x):
        return {"serialize": True, "type": object}

    def Color(self, fg=None, bg=None):
        fg = fg or self.FG_COLOR
        if fg is not None:
            fg = fg.strip()
            if not fg.startswith('#'):
                raise FTMonoaRuntimeUnexpectedColor(self.cmonoa, f"Foreground color must be in #RRGGBB format. but got fg={fg}")
            fg = QColor(fg)
            fg.setAlpha(self.FG_ALPHA)
        bg = bg or self.BG_COLOR
        if bg is not None:
            bg = bg.strip()
            if not bg.startswith('#'):
                raise FTMonoaRuntimeUnexpectedColor(self.cmonoa, f"Background color must be in #RRGGBB format. but got bg={bg}")
            bg = QColor(bg)
            bg.setAlpha(self.BG_ALPHA)
        return {"color": (fg, bg)}

    def Tooltip(self, x):
        return {"tooltip": x}

    def Label(self, x):
        return {"label": x}

    def Group(self, x=None):
        if x is not None:
            if not isinstance(x, (str, int)):
                raise FTMonoaRuntimeEvalError(self.cmonoa, f"Group name must be str or int. but got group={x}, type={type(x)}")
        return {"group": x}

    def Header(self, x):
        return {"header": x}

    def Readonly(self):
        return {"readonly": True}

    def Separator(self):
        return {"separator": True}

    def Space(self, x=20):
        if x is not None:
            if not isinstance(x, int):
                raise FTMonoaRuntimeEvalError(self.cmonoa, f"Space height must be int. but got space={x}, type={type(x)}")
        return {"space": x}

    def _check_range_with_type(self, _range, _type):
        """
        * 当描述符与Type(int|float)结合并且S的类型不匹配时，会抛出异常
        * 当描述符与Type(str|bool)结合时，会抛出异常
        """
        if _range is None:
            return True
        start, stop, step = _range.start, _range.stop, _range.step
        start, stop, step = start if start is not None else 0, stop, step if step is not None else 1
        if _type == int:
            if not isinstance(start, int):
                raise FTMonoaRuntimeDismatchedRangeType(self.cmonoa, f"Type of range.start must be int. but got range.start={start}")
            if not isinstance(stop, int):
                raise FTMonoaRuntimeDismatchedRangeType(self.cmonoa, f"Type of range.stop must be int. but got range.stop={stop}")
            if not isinstance(step, int):
                raise FTMonoaRuntimeDismatchedRangeType(self.cmonoa, f"Type of range.step must be int. but got range.step={step}")
        elif _type == float:
            if isinstance(start, int):
                start = float(start)
            elif not isinstance(start, float):
                raise FTMonoaRuntimeDismatchedRangeType(self.cmonoa, f"Type of range.start must be float. but got range.start={start}")
            if isinstance(stop, int):
                stop = float(stop)
            elif not isinstance(stop, float):
                raise FTMonoaRuntimeDismatchedRangeType(self.cmonoa, f"Type of range.stop must be float. but got range.stop={stop}")
            if isinstance(step, int):
                step = float(step)
            elif not isinstance(step, float):
                raise FTMonoaRuntimeDismatchedRangeType(self.cmonoa, f"Type of range.step must be float. but got range.step={step}")
        else:
            raise FTMonoaRuntimeEvalError(self.cmonoa, f"Type '{_type}' is not supported for Range.")
        return True


    def _check_enum_with_type(self, _enum, _type, _value):
        """
        * 当描述符与Type(int|float|str)结合时，提升QXXX为QComboBox
        * 当描述符与Type(bool)结合时，会抛出异常
        """
        if _enum is None:
            return True
        if _type == bool:
            raise FTMonoaRuntimeEvalError(self.cmonoa, f"Type '{_type}' is not supported for Enum.")
        elif _type == str:
            if _value not in _enum:
                _enum.insert(0, _value)

        # check each one
        for e in _enum:
            if not isinstance(e, _type):
                raise FTMonoaRuntimeDismatchedEnumType(self.cmonoa, f"Type of Enum must be {_type}. but got Enum={_enum}")

        return True

    def __call__(self, monoa:MonoAttr, monoe:dict) -> tuple[dict, dict]:
        """
        解析一个MonoAttr对象，返回一个dict对象，包含了关键属性的顺序信息; 以及一个dict对象，包含了所有的属性信息。
        """
        monoa.iterall(_api_prehandle_single_attr)
        idxs, res, self.cmonoa = {}, {}, monoa
        _idx, env = 0, monoe.copy()
        env.update(self.monoa_env)
        for expression in monoa:
            try:
                _ = eval(expression, env)
            except Exception as e:
                env = self._remove_builtins(env)
                raise FTMonoaRuntimeEvalError(self.cmonoa, f"Error while evaluating expression: {expression} - {e}\n\n\tcurrent environ: {env}")
            res.update(_)

            # record idx
            key = list(_)[0]
            idxs[key] = _idx
            _idx += 1

        # add name and value
        res['name'] = monoa.name
        res['value'] = monoa.value

        # fill default values
        for k, v in self.DEFAULTS.items():
            if k not in res:
                res[k] = v

        # check type
        if res['type'] is None and monoa.value is None:
            res['type'] = str
            monoa.value = ""
        else:
            is_monoa_value_valid = isinstance(monoa.value, (int, float, str, bool))
            if not is_monoa_value_valid and res['type'] != object:
                raise FTMonoaRuntimeEvalError(self.cmonoa, f"Type '{type(monoa.value)}' of value '{monoa.value}' is not supported.")
            if res['type'] is None:
                res['type'] = type(monoa.value) if is_monoa_value_valid else object
            if res['type'] != type(monoa.value) and res['type'] != object:
                try:
                    monoa.value = res['type'](monoa.value)
                except Exception as e:
                    raise FTMonoaRuntimeEvalError(self.cmonoa, f"Type '{res['type']}' is not supported.")
            if _is_builtin_instance(monoa.value) and res['type'] == object:
                raise FTMonoaRuntimeEvalError(self.cmonoa, f"Type '{type(monoa.value)}' of value '{monoa.value}' is not support to be serialized(Type(object) or Serialize it).")
        # cross check
        self._check_range_with_type(res['range'], res['type'])
        self._check_enum_with_type(res['enum'], res['type'], monoa.value)

        return idxs, res


def _api_prehandle_single_attr(attr:str):
    """
    每一条attr都应当为一条python函数执行语句，所以第一步是补全()
    """
    attr = attr.strip()
    # re check
    if attr.endswith(')'):
        return attr
    return attr + '()'


def _api_diagnose_attr_type(obj, monoa:MonoAttr):
    param, value = monoa.name, monoa.value

    for attr in monoa:
        attr = attr.lower()


MONO_FONT = QFont('Consolas', 12, QFont.Bold)
MONO_HEADER_FONT = QFont('Consolas', 14, QFont.Bold)

class QMonoWithoutBorder:
    ...

class QMonoRectBorder(QMonoWithoutBorder):
    ...

class QMonoRoundRectBorder(QMonoWithoutBorder):
    ...


class QMonoWidget(QWidget):
    def __init__(self, attr_dict:dict, parent=None, *, border=QMonoWithoutBorder):
        super().__init__(parent)
        self.ad = attr_dict  # attr_dict
        self._name = self.ad['name']
        self._value = self.ad['value']
        self._rootL = QVBoxLayout()
        self._rootL.setContentsMargins(4, 4, 6, 6)
        self._rootL.setSpacing(4)
        self._mainL = QHBoxLayout()
        self._mainL.setContentsMargins(2, 2, 4, 4)
        self._mainL.setSpacing(2)
        self.setLayout(self._rootL)
        self._rootL.addLayout(self._mainL)
        self._border = border
        assert issubclass(self._border, QMonoWithoutBorder), f"Border must be subclass of QMonoWithoutBorder."

        # ---
        self._uis = []
        self._int_float_vc_flag = False
        self._bool_vc_flag = False
        self._str_vc_flag = False

        self._create_ui()

        # --- set default value
        self._set_default_value()


    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    def _set_default_value(self, *_):
        if self.ad['type'] in (float, int):
            self._int_float_value_changed(self.ad['value'])
        elif self.ad['type'] == bool:
            self._bool_value_changed(self.ad['value'])
        elif self.ad['type'] == str:
            self._str_value_changed(self.ad['value'])
        else:
            raise FTQMonoWidgetRecvObjectError(f"Type of object is not supported in single QMonoWidget.")

    def _select_main_widget(self):
        if self.ad['type'] == int:
            return QSpinBox
        elif self.ad['type'] == float:
            return QDoubleSpinBox
        elif self.ad['type'] == str:
            return QLineEdit
        elif self.ad['type'] == bool:
            return QCheckBox
        elif self.ad['type'] == object:
            raise FTQMonoWidgetRecvObjectError(f"Type of object is not supported in single QMonoWidget.")
        else:
            raise TypeError(f"Type '{self.ad['type']}' is not supported.")

    def _create_ui(self):
        self._lbl = QLabel((self.ad['label'] if self.ad['label'] else self.ad['name']))
        self._lbl.setFont(MONO_FONT)
        self._mainL.addWidget(self._lbl)

        self._mwd = self._select_main_widget()()
        self._mwd.setFont(MONO_FONT)
        self._mainL.addWidget(self._mwd)

        self._btn = QPushButton("O")
        self._btn.setFont(QFont('Arial', 10))
        self._btn.setFixedSize(20, 20)
        self._btn.clicked.connect(self._set_default_value)
        self._mainL.addWidget(self._btn)

        # check range
        if self.ad['range'] and not self.ad['enum']:  # python range
            assert isinstance(self._mwd, (QSpinBox, QDoubleSpinBox)), f"Range is not supported for type '{self.ad['type']}'"
            start, stop, step = self.ad['range'].start, self.ad['range'].stop, self.ad['range'].step
            start, stop, step = start if start is not None else 0, stop, step if step is not None else 1
            self._mwd.setRange(start, stop)
            self._mwd.setSingleStep(step)

            self._qsl = QIntSlider(Qt.Horizontal, start, stop, step) if self.ad['type'] == int else QDoubleSlider(Qt.Horizontal, start, stop, step)
            self._qsl.monoChanged.connect(self._int_float_value_changed)
            self._uis.append(self._qsl)
            self._rootL.addWidget(self._qsl)
        else:
            self._qsl = None

        # check enum
        if self.ad['enum']:
            assert isinstance(self._mwd, (QSpinBox, QDoubleSpinBox, QLineEdit)), f"Enum is not supported for type '{self.ad['type']}'"
            self._mcb = QComboBox()
            self._mcb.setFont(MONO_FONT)
            self._mcb.addItems([str(it) for it in self.ad['enum']])
            self._mcb.currentIndexChanged.connect(self._combo_value_changed)
            self._uis.append(self._mcb)
            self._rootL.addWidget(self._mcb)

            # as readonly
            self._mwd.setReadOnly(True)
        else:
            self._mcb = None

        # posthandle
        self._uis.append(self._lbl)
        self._uis.append(self._mwd)
        self._uis.append(self._btn)

        # transparent
        for ui in self._uis:
            ui.setAttribute(Qt.WA_TranslucentBackground)

        # re label
        if self.ad['label']:
            self._lbl.setText(self.ad['label'])

        # readonly
        if self.ad['readonly']:
            for ui in self._uis:
                if hasattr(ui, 'setReadOnly'):
                    ui.setReadOnly(True)
                else:
                    ui.setEnabled(False)

        # tooltips
        if self.ad['tooltip']:
            for ui in self._uis:
                ui.setToolTip(self.ad['tooltip'])

        # color
        if self.ad['color']:  # fg, bg
            fg, bg = self.ad['color']
            for ui in self._uis:
                if isinstance(ui, (QLineEdit, QSpinBox, QDoubleSpinBox, QPushButton, QComboBox)):
                    continue
                txt = ""
                if fg is not None:
                    txt += f"color:rgba({fg.red()}, {fg.green()}, {fg.blue()}, {fg.alpha()});"
                if bg is not None:
                    txt += f"{ui.__class__.__name__}" + "{" + f"background-color:rgba({bg.red()}, {bg.green()}, {bg.blue()}, {bg.alpha()}); + " + "}"
                    txt += f"{ui.__class__.__name__}:focus" + "{" + f"background-color:rgba({bg.red()}, {bg.green()}, {bg.blue()}, {bg.alpha()}); + " + "}"

                ui.setStyleSheet(txt)

        if isinstance(self._mwd, (QSpinBox, QDoubleSpinBox)):
            self._mwd.valueChanged.connect(self._int_float_value_changed)
        elif isinstance(self._mwd, QCheckBox):
            self._mwd.setText("")
            self._mwd.setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px; };" + self._mwd.styleSheet())
            self._mwd.setMaximumSize(20, 20)
            self._mwd.stateChanged.connect(self._bool_value_changed)
        elif isinstance(self._mwd, QLineEdit):
            self._mwd.textChanged.connect(self._str_value_changed)
    def _int_float_value_changed(self, value, *args):
        if self._int_float_vc_flag: return
        self._int_float_vc_flag = True

        if self._mcb:  # check this first
            if value in self.ad['enum']:
                self._mcb.setCurrentIndex(self.ad['enum'].index(value))
            else:
                idx, value = find_closest(value, self.ad['enum'])
                self._mcb.setCurrentIndex(idx)

        self._mwd.setValue(value)
        if self._qsl:
            self._qsl.setValue(value)

        self._value = value
        self._int_float_vc_flag = False

    def _bool_value_changed(self, value):
        if self._bool_vc_flag: return
        self._bool_vc_flag = True

        self._mwd.setChecked(value)
        self._value = value

        self._bool_vc_flag = False

    def _str_value_changed(self, value):
        if self._str_vc_flag: return
        self._str_vc_flag = True

        self._mwd.setText(value)
        self._value = value

        self._str_vc_flag = False

    def _combo_value_changed(self, index):
        value = self.ad['enum'][index]
        if isinstance(self._mwd, (QSpinBox, QDoubleSpinBox)):
            self._int_float_value_changed(value)
        elif isinstance(self._mwd, QLineEdit):
            self._str_value_changed(value)
        else:
            raise TypeError(f"Type '{self.ad['type']}' is not supported with checkbox.")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 获取窗口的大小
        rect = self.rect()
        rect.adjust(0, 0, -4, -4)

        # # 绘制底色
        # base_color = QColor("#888888")
        # base_color.setAlpha(200)
        # painter.setPen(QPen(base_color, 1, Qt.SolidLine))
        # painter.setBrush(Qt.NoBrush)
        # painter.translate(1, 1)  # 偏移
        # painter.drawRoundedRect(rect, 4, 4)
        # base_color.setAlpha(100)
        # painter.translate(1, 1)  # 偏移
        # painter.drawRoundedRect(rect, 4, 4)
        # painter.translate(-2, -2)  # 恢复原位置


        # 设置阴影的颜色和透明度
        shadow_color = QColor("#848080")
        shadow_color.setAlpha(50)
        shadow_fill_color = QColor("#FFFF00") if (self.ad['color'] is None or self.ad['color'][1] is None) else self.ad['color'][1]
        shadow_fill_color.setAlpha(25)
        # 融合颜色


        # 绘制底色
        painter.translate(3, 3)
        painter.setPen(QPen(shadow_color, 1, Qt.SolidLine))
        painter.setBrush(QBrush(shadow_fill_color))
        painter.drawRoundedRect(rect, 4, 4)
        painter.translate(-3, -3)  # 恢复原位置

        # 绘制圆角矩形边框
        border_color = QColor("#000000")
        border_color.setAlpha(150)
        painter.setPen(QPen(border_color, 1, Qt.SolidLine))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect, 4, 4)
        painter.translate(1, 1)
        border_color.setAlpha(100)
        painter.setPen(QPen(border_color, 1, Qt.SolidLine))
        painter.drawRoundedRect(rect, 4, 4)
        painter.translate(1, 1)
        border_color.setAlpha(50)
        painter.setPen(QPen(border_color, 1, Qt.SolidLine))
        painter.drawRoundedRect(rect, 4, 4)
        painter.translate(-2, -2)


        # 在这里添加其他绘制逻辑
        # ...

        # 调用基类的 paintEvent 以进行正常的绘制
        super().paintEvent(event)


class QMonoSeparator(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(1)

class QMonoSpacer(QWidget):
    def __init__(self, height:int=20, parent=None):
        super().__init__(parent)
        self.setFixedHeight(height)

QMONO_INSPECTOR_TITLE_COLOR = QColor(32, 144, 245, 225)
QMONO_INSPECTOR_TITLE_SHDCOLOR = QColor(8, 38, 61, 225)
QMONO_INSPECTOR_TITLE_FONT = QFont('Consolas', 16, QFont.Bold)

class QMonoInspector(QWidget):
    def __init__(self, mono_target:Mono, parent=None):
        super().__init__(parent)
        self._raw = mono_target.monos
        mra = MonoaRuntime()
        self._monos = []
        self._idxs = []
        for m in self._raw:
            idxs, mono = mra(m, mono_target.env)
            self._idxs.append(idxs)
            self._monos.append(mono)

        self._mono_widgets = []
        self._rootL = QVBoxLayout()
        self._rootL.setContentsMargins(2, 2, 0, 2)
        self._rootL.setSpacing(2)
        self.setLayout(self._rootL)

        self._create_ui()

    @property
    def monos(self):
        return self._monos

    @staticmethod
    def _get_inspector_attrs(attr:dict) -> tuple[str|int|None, str|None, int|None, bool, bool]|None:
        group = attr['group']
        header = attr['header']
        space = attr['space']
        separator = attr['separator']
        serialize = attr['serialize']
        if group or header or space or separator or serialize:
            return group, header, space, separator, serialize
        return None

    def _add_mono_title(self, title:str="Mono Inspector:"):
        _l = QHBoxLayout()
        w = QShadowLabel(title, QMONO_INSPECTOR_TITLE_COLOR, QMONO_INSPECTOR_TITLE_SHDCOLOR, 2)
        w.setFont(QMONO_INSPECTOR_TITLE_FONT)
        _l.addWidget(w)
        # add a space
        _l.addStretch()
        self._rootL.addLayout(_l)

    def _add_header(self, title:str=""):
        _l = QHBoxLayout()
        w = QLabel(title)
        w.setFont(MONO_HEADER_FONT)
        _l.addWidget(w)
        # add a space
        _l.addStretch()
        self._rootL.addLayout(_l)

    def _add_separator(self):
        w = QMonoSeparator(self)
        self._rootL.addWidget(w)

    def _add_space(self, height:int=20):
        w = QMonoSpacer(height)
        self._rootL.addWidget(w)

    def _pre_create_of_the_mono(self, m_idx, m):
        # inspector check
        inspect_attrs = self._get_inspector_attrs(m)

        if inspect_attrs is not None:
            this_idxs = self._idxs[m_idx]
            keys = ['group', 'header', 'space', 'separator', 'serialize']
            idxs = this_idxs.get('group', -1), this_idxs.get('header', -1), this_idxs.get('space', -1), this_idxs.get('separator', -1), this_idxs.get('serialize', -1)
            loopfor_dict = {}  # int: tuple[str, any]
            for i, k in enumerate(keys):
                if idxs[i] == -1:
                    continue
                loopfor_dict[this_idxs[k]] = (k, inspect_attrs[i])
            # sort
            loopfor_dict = dict(sorted(loopfor_dict.items(), key=lambda x: x[0]))

            # loop
            for idx, (k, v) in loopfor_dict.items():
                if k == 'group' and v is not None:
                    # group TODO: add group
                    pass
                elif k == 'header' and v is not None:
                    self._add_header(v)
                elif k == 'space' and v is not None:
                    self._add_space(v)
                elif k == 'separator' and v is True:
                    self._add_separator()
                elif k == 'serialize' and v is True:
                    continue

    def _create_ui(self):
        self._add_mono_title("Mono Inspector:")

        for i, m in enumerate(self._monos):
            self._pre_create_of_the_mono(i, m)
            w = QMonoWidget(m)
            self._mono_widgets.append(w)
            self._rootL.addWidget(w)

    @property
    def params(self):
        res = {}
        for w in self._mono_widgets:
            res[w.name] = w.value
        return res

    def closeEvent(self, a0):
        print("Inspector closed. Params:\n\t", self.params)
        self.close()

def _TestSingleUI(monoa:MonoAttr, monoe:dict):
    mar = MonoaRuntime()
    attr_dict = mar(monoa, monoe)
    print("Parsed :\t")
    for k, v in attr_dict.items():
        print(f"\t{k}:\t{v}")
    app = QApplication(sys.argv)
    w = QMonoWidget(attr_dict)
    w.setWindowTitle("Test")
    w.show()
    sys.exit(app.exec_())

def _TestInspector(mono:Mono):
    app = QApplication(sys.argv)
    w = QMonoInspector(mono)
    w.setWindowTitle("Test")
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    mono = Mono(
        "//\s*>", "\n",
        "\$", "\$",
        None, "//\s*<",
        "//\s*\[", "\]",
        "//\s*\?", '//\s*:\?', "//\s*:", "//\s*\$",
        COMMENT=r";#", CSO=r"/*#", CEO=r"\*/",
        ENV=r"import math"
    )

    with open('counter.v5.v', 'r', encoding="utf-8") as f:
        test = f.read()

    with open('saved.v', 'w', encoding="utf-8") as f:
        f.write(mono.handle(test, WIDTH=10, add_en=True))

    # test1
    # monos = mono.monos
    # if len(monos) > 0:
    #     one = monos[0]
    #     print(f"mono-attr:\t{one}")
    #     _TestSingleUI(one, mono.env)

    # test2
    _TestInspector(mono)