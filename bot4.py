import telebot
from sympy import symbols, Eq, solve, sympify, diff, integrate, limit, Matrix, det, dsolve, Function
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re

# توکن ربات
BOT_TOKEN = '7799600612:AAETLSphASwA8_OWHBAVe2B2aB7N6l5uB5E'
bot = telebot.TeleBot(BOT_TOKEN)

# پیام خوش‌آمدگویی (/start)
start_text = """
✦━─━───━✦🌟✦━───━─━✦

👋✨ سلام! به این ربات خوش اومدی ✨👋

این ربات توسط: @ureof ساخته شده 🛠️

📚 قبل از نوشتن هر معادله‌ای، حتماً راهنمای ربات رو بخون:

/guide

تا بدونی چطور باید عبارت ریاضی رو درست وارد کنی ✅

✦━─━───━✦🌟✦━───━─━✦
"""

# پیام راهنما (/guide) - اصلاح‌شده برای رفع ارور Markdown
guide_text = """
📚✦━━━━━━━✦📚
راهنمای ربات حل‌کننده ریاضی
📚✦━━━━━━━✦📚

من ربات ریاضی هستم و تقریباً همه‌چیز رو حل می‌کنم 😎

━━━━━━━━━━━━━━━
🧮 نحوه عملکرد در گروه‌ها
━━━━━━━━━━━━━━━
➊ فقط کافیه `/math` بنویسی و بعدش عبارت ریاضی رو وارد کنی.
همین! من حل می‌کنم ✅

━━━━━━━━━━━━━━━
🧮 نحوه عملکرد در پی‌وی
━━━━━━━━━━━━━━━
➊ فقط عبارت ریاضیت رو بفرست…
بوممم 💥 جوابو می‌گیری!

━━━━━━━━━━━━━━━
🤔 چطور عبارت‌ها رو بنویسی؟
━━━━━━━━━━━━━━━
✦ علامت‌های اصلی:
`=` ➝ تساوی
`*` ➝ ضرب
`/` ➝ تقسیم
`**` ➝ توان
•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•
✦ توابع ریاضی:
∘ مثلثاتی: `sin(x)`, `cos(x)`, `tan(x)`  
  سینوس، کسینوس، تانژانت
━━━━━━━━━━━━━━━
∘ لگاریتم: `ln(x)` (طبیعی)، `log(x,10)` (پایه ۱۰)
━━━━━━━━━━━━━━━
∘ جذر: `sqrt(x)`

∘ ریشه‌های بالاتر: `nthroot(x,n)`  

مثال: `nthroot(8,3)` ➝ ریشه سوم ۸
━━━━━━━━━━━━━━━
∘ نمایی: `exp(x)` ➝ \( e^x \)
•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•
✦ متغیرها:
∘ از حروف ساده مثل `x`, `y`, `z` استفاده کن.
•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•
✦ پرانتز:
∘ برای عبارات پیچیده‌تر. مثال: `(x+1)**2`
•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•
✦ ماتریس:
∘ مثل `[[3,4],[1,2]]`
•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•
✦ دیفرانسیل:
∘ `y'` ➝ مشتق اول
∘ `y''` ➝ مشتق دوم

━━━━━━━━━━━━━━━
📌 نکات مهم
━━━━━━━━━━━━━━━
•در انتگرال/حد، بین مقادیر `,` (کاما لاتین) بگذار.
•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•
•در گروه همیشه اول `/math` بنویس.
•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•
•اگه خطا گرفتی: فرمت رو چک کن یا `/guide` بزن.

━━━━━━━━━━━━━━━
✅ خب… حالا معادله‌تو بفرست تا شروع کنیم!
━━━━━━━━━━━━━━━
"""

# خوش‌آمدگویی
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, start_text, parse_mode='Markdown')

# راهنما
@bot.message_handler(commands=['guide'])
def guide_message(message):
    bot.send_message(message.chat.id, guide_text, parse_mode='Markdown')

# منوی کمک
@bot.message_handler(commands=['help'])
def help_message(message):
    help_text = """
📋 **دستورات ربات**:
- **گروه**: فقط `/math` (مثل `/math x**2 = 4`)
- **پی‌وی**: مستقیم عبارت بنویس (مثل `x^2 = 4`)
- خودم نوع مسئله رو تشخیص می‌دم (معادله، انتگرال، مشتق، حد، ماتریس، دیفرانسیل)
- `/guide` → راهنمای کامل با مثال
🌟 تو گروه فقط `/math` کار می‌کنه!
"""
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

# تشخیص نوع مسئله و حل
def solve_math(expr, message):
    try:
        expr = expr.strip()
        
        # 1. معادلات دیفرانسیل (اگر y' یا y'' باشه)
        if "y'" in expr or "y''" in expr:
            if '=' in expr:
                left, right = expr.split('=', 1)
                left = sympify(left.strip(), evaluate=False)
                right = sympify(right.strip(), evaluate=False)
                eq = Eq(left, right)
                y = symbols('y', cls=Function)
                x = symbols('x')
                result = dsolve(eq, y(x))
                bot.send_message(message.chat.id, f"**حل دیفرانسیل**: {result}", parse_mode='Markdown', reply_to_message_id=message.message_id)
            else:
                bot.send_message(message.chat.id, "**خطا**: معادله دیفرانسیل باید با = نوشته بشه!", parse_mode='Markdown', reply_to_message_id=message.message_id)
            return

        # 2. ماتریس (اگر [[ باشه)
        if '[[' in expr and ']]' in expr:
            parts = expr.split(' ', 1)
            op = parts[0].strip().lower() if len(parts) > 1 else 'det'
            matrix_str = parts[1].strip() if len(parts) > 1 else expr
            matrix_str = re.sub(r'\s+', '', matrix_str)
            rows = matrix_str.strip('[]').split('],[')
            matrix_data = []
            for row in rows:
                row = row.replace('[', '').replace(']', '')
                matrix_data.append([sympify(x) for x in row.split(',')])
            M = Matrix(matrix_data)
            if op == 'det':
                result = det(M)
                bot.send_message(message.chat.id, f"**دترمینان**: {result}", parse_mode='Markdown', reply_to_message_id=message.message_id)
            elif op == 'inv':
                result = M.inv()
                bot.send_message(message.chat.id, f"**معکوس**: {result}", parse_mode='Markdown', reply_to_message_id=message.message_id)
            else:
                bot.send_message(message.chat.id, "**عملیات**: det یا inv", parse_mode='Markdown', reply_to_message_id=message.message_id)
            return

        # 3. حد (اگر , و -> باشه یا تعداد کاما >= 2)
        if ',' in expr and ('->' in expr or expr.count(',') >= 2):
            parts = expr.split(',')
            expr_str = parts[0].strip()
            var_str = parts[1].strip()
            value_str = parts[2].strip() if len(parts) > 2 else '0'
            dir_str = parts[3].strip() if len(parts) > 3 else '+'
            if '->' in var_str:
                var_str, value_str = var_str.split('->')
                var_str = var_str.strip()
                value_str = value_str.strip()
            expr_sym = sympify(expr_str)
            var = symbols(var_str)
            result = limit(expr_sym, var, sympify(value_str), dir=dir_str)
            bot.send_message(message.chat.id, f"**حد**: {result}", parse_mode='Markdown', reply_to_message_id=message.message_id)
            return

        # 4. انتگرال (اگر , باشه و نه ->)
        if ',' in expr and '->' not in expr and expr.count(',') < 2:
            parts = expr.split(',')
            expr_str = parts[0].strip()
            var_str = parts[1].strip() if len(parts) > 1 else 'x'
            limits = None
            if len(parts) > 2:
                lower = sympify(parts[2].strip())
                upper = sympify(parts[3].strip()) if len(parts) > 3 else None
                limits = (symbols(var_str), lower, upper) if upper else (symbols(var_str), lower)
            expr_sym = sympify(expr_str)
            var = symbols(var_str)
            result = integrate(expr_sym, limits if limits else var)
            bot.send_message(message.chat.id, f"**انتگرال**: {result}", parse_mode='Markdown', reply_to_message_id=message.message_id)
            return

        # 5. مشتق (اگر diff باشه)
        if expr.lower().startswith('diff'):
            parts = expr.split(' ', 1)[1].split(',')
            expr_str = parts[0].strip()
            wrt_str = parts[1].strip() if len(parts) > 1 else 'x'
            expr_sym = sympify(expr_str)
            var = symbols(wrt_str)
            result = diff(expr_sym, var)
            bot.send_message(message.chat.id, f"**مشتق**: {result}", parse_mode='Markdown', reply_to_message_id=message.message_id)
            return

        # 6. معادله (اگر = باشه یا عبارت ساده)
        if '=' in expr:
            left, right = expr.split('=', 1)
            left = sympify(left.strip(), evaluate=False)
            right = sympify(right.strip(), evaluate=False)
            eq = Eq(left, right)
            vars = list(eq.free_symbols)
            if not vars:
                raise ValueError("معادله متغیر نداره!")
            solutions = solve(eq, vars[0]) if len(vars) == 1 else solve(eq, vars)
            bot.send_message(message.chat.id, f"**حل**: {solutions}", parse_mode='Markdown', reply_to_message_id=message.message_id)
        else:
            expr_sym = sympify(expr, evaluate=False)
            vars = list(expr_sym.free_symbols)
            solutions = solve(expr_sym, vars[0]) if vars else expr_sym.evalf()
            bot.send_message(message.chat.id, f"**حل**: {solutions}", parse_mode='Markdown', reply_to_message_id=message.message_id)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ **خطا**: {str(e)}\nمثال: `/math x**2 = 4`\nراهنما: `/guide`", parse_mode='Markdown', reply_to_message_id=message.message_id)

# حل‌کننده برای گروه (فقط /math با ریپلای)
@bot.message_handler(commands=['math'], func=lambda message: message.chat.type in ['group', 'supergroup'])
def math_group_handler(message):
    try:
        expr = message.text.split(' ', 1)[1]
        solve_math(expr, message)
    except:
        bot.send_message(message.chat.id, "❌ **لطفاً عبارت ریاضی بنویس!**\nمثال: `/math x**2 = 4`\nراهنما: `/guide`", parse_mode='Markdown', reply_to_message_id=message.message_id)

# حل‌کننده برای چت خصوصی (بدون دستور)
@bot.message_handler(func=lambda message: message.chat.type == 'private')
def math_private_handler(message):
    solve_math(message.text, message)

# هندلر عمومی برای گروه (ایگنور پیام‌های بدون /math)
@bot.message_handler(func=lambda message: message.chat.type in ['group', 'supergroup'])
def ignore_group(message):
    pass  # کامل ایگنور می‌کنه

if __name__ == '__main__':
    print("ربات ریاضی شروع شد...")
    bot.infinity_polling()