"""
AI Email Assistant
مساعد البريد الإلكتروني بالذكاء الاصطناعي
يستخدم Claude API لمساعدتك في كتابة وترجمة وتلخيص الإيميلات
"""

import os
import sys
from anthropic import Anthropic


class EmailAssistant:
    """مساعد الإيميل بالذكاء الاصطناعي"""

    def __init__(self, api_key: str = None):
        """تهيئة المساعد"""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "❌ لم يتم العثور على API key. "
                "ضعيها في متغير البيئة ANTHROPIC_API_KEY أو مرريها للدالة."
            )
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"

    def _send_request(self, prompt: str, max_tokens: int = 1024) -> str:
        """إرسال طلب إلى Claude API"""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            return f"❌ حدث خطأ: {str(e)}"

    def compose_email(self, points: str, tone: str = "رسمي",
                      language: str = "العربية") -> str:
        """
        كتابة إيميل بناءً على نقاط

        Args:
            points: النقاط الأساسية للإيميل
            tone: النبرة (رسمي، ودي، حيادي)
            language: لغة الإيميل (العربية أو الإنجليزية)
        """
        prompt = f"""أنت مساعد احترافي لكتابة رسائل البريد الإلكتروني.

اكتب إيميل بلغة {language} وبنبرة {tone} بناءً على هذه النقاط:

{points}

متطلبات:
- اكتب موضوعاً مناسباً (Subject)
- استخدم تحية مناسبة للنبرة المطلوبة
- نظّم المحتوى بفقرات واضحة
- اختم بتحية ختامية مناسبة
- اجعل الإيميل موجزاً ومهنياً

الصيغة:
Subject: [الموضوع]

[محتوى الإيميل]"""

        return self._send_request(prompt, max_tokens=1500)

    def translate_email(self, email_text: str, target_language: str = "English") -> str:
        """
        ترجمة إيميل للغة أخرى مع الحفاظ على الطابع المهني
        """
        prompt = f"""ترجم هذا الإيميل إلى {target_language} بأسلوب مهني ومحترف،
مع الحفاظ على المعنى والنبرة الأصلية:

الإيميل الأصلي:
{email_text}

قدم الترجمة فقط بدون إضافات أو شرح."""

        return self._send_request(prompt, max_tokens=1500)

    def summarize_email(self, email_text: str) -> str:
        """تلخيص إيميل طويل في نقاط مختصرة"""
        prompt = f"""لخّص هذا الإيميل في نقاط واضحة ومختصرة بالعربية:

{email_text}

الصيغة المطلوبة:
📧 **الموضوع الرئيسي:** [جملة قصيرة]

🎯 **النقاط الأساسية:**
• [نقطة 1]
• [نقطة 2]
• [نقطة 3]

⚡ **المطلوب منك:** [الإجراء المطلوب، أو "لا يوجد إجراء مطلوب"]

⏰ **الإلحاح:** [عاجل / متوسط / غير عاجل]"""

        return self._send_request(prompt, max_tokens=800)

    def suggest_reply(self, email_text: str, reply_type: str = "قبول") -> str:
        """
        اقتراح رد مناسب على إيميل

        Args:
            email_text: نص الإيميل الأصلي
            reply_type: نوع الرد (قبول، رفض مهذب، طلب توضيح، تأجيل)
        """
        prompt = f"""اقرأ هذا الإيميل واكتب رداً مهنياً مناسباً.

الإيميل الأصلي:
{email_text}

نوع الرد المطلوب: {reply_type}

متطلبات الرد:
- ابدأ بتحية مناسبة
- أظهر الاهتمام والاحترام للمرسل
- كن واضحاً ومختصراً
- اختم بتحية ختامية مهنية
- استخدم نفس لغة الإيميل الأصلي"""

        return self._send_request(prompt, max_tokens=1000)


def print_menu():
    """طباعة القائمة الرئيسية"""
    print("\n" + "="*55)
    print("       📧 مساعد البريد الإلكتروني بالذكاء الاصطناعي")
    print("="*55)
    print("\n1️⃣  كتابة إيميل جديد")
    print("2️⃣  ترجمة إيميل")
    print("3️⃣  تلخيص إيميل")
    print("4️⃣  اقتراح رد")
    print("5️⃣  خروج")
    print("-"*55)


def get_multiline_input(prompt: str) -> str:
    """قراءة نص متعدد الأسطر من المستخدم"""
    print(f"\n{prompt}")
    print("(اكتبي النص، ثم اضغطي Enter مرتين للإنهاء)")
    lines = []
    empty_count = 0
    while True:
        try:
            line = input()
            if line == "":
                empty_count += 1
                if empty_count >= 1 and lines:
                    break
            else:
                empty_count = 0
                lines.append(line)
        except EOFError:
            break
    return "\n".join(lines)


def main():
    """الدالة الرئيسية"""
    try:
        assistant = EmailAssistant()
    except ValueError as e:
        print(e)
        print("\n💡 للحصول على API key:")
        print("   1. اذهبي إلى: https://console.anthropic.com")
        print("   2. أنشئي حساباً واحصلي على مفتاح API")
        print("   3. عرّفي متغير البيئة:")
        print("      export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)

    while True:
        print_menu()
        choice = input("\nاختاري رقماً: ").strip()

        if choice == "1":
            print("\n✍️ كتابة إيميل جديد")
            print("-" * 40)
            points = get_multiline_input("📝 اكتبي النقاط الأساسية للإيميل:")

            print("\nاختاري النبرة:")
            print("  1. رسمي  2. ودي  3. حيادي")
            tone_choice = input("النبرة (1-3): ").strip()
            tones = {"1": "رسمي", "2": "ودي", "3": "حيادي"}
            tone = tones.get(tone_choice, "رسمي")

            print("\nاختاري اللغة:")
            print("  1. العربية  2. English")
            lang_choice = input("اللغة (1-2): ").strip()
            language = "English" if lang_choice == "2" else "العربية"

            print("\n⏳ جاري الكتابة...\n")
            result = assistant.compose_email(points, tone, language)
            print("="*55)
            print(result)
            print("="*55)

        elif choice == "2":
            print("\n🔄 ترجمة إيميل")
            print("-" * 40)
            email = get_multiline_input("📧 الصقي الإيميل للترجمة:")

            print("\nاختاري لغة الترجمة:")
            print("  1. English  2. العربية  3. Français")
            lang_choice = input("اللغة (1-3): ").strip()
            langs = {"1": "English", "2": "العربية", "3": "Français"}
            target = langs.get(lang_choice, "English")

            print("\n⏳ جاري الترجمة...\n")
            result = assistant.translate_email(email, target)
            print("="*55)
            print(result)
            print("="*55)

        elif choice == "3":
            print("\n📝 تلخيص إيميل")
            print("-" * 40)
            email = get_multiline_input("📧 الصقي الإيميل للتلخيص:")

            print("\n⏳ جاري التلخيص...\n")
            result = assistant.summarize_email(email)
            print("="*55)
            print(result)
            print("="*55)

        elif choice == "4":
            print("\n💬 اقتراح رد")
            print("-" * 40)
            email = get_multiline_input("📧 الصقي الإيميل للرد عليه:")

            print("\nاختاري نوع الرد:")
            print("  1. قبول  2. رفض مهذب  3. طلب توضيح  4. تأجيل")
            type_choice = input("النوع (1-4): ").strip()
            types = {
                "1": "قبول",
                "2": "رفض مهذب",
                "3": "طلب توضيح",
                "4": "تأجيل"
            }
            reply_type = types.get(type_choice, "قبول")

            print("\n⏳ جاري كتابة الرد...\n")
            result = assistant.suggest_reply(email, reply_type)
            print("="*55)
            print(result)
            print("="*55)

        elif choice == "5":
            print("\n👋 مع السلامة! نتمنى لكِ يوماً منتجاً 🌸\n")
            break

        else:
            print("\n❌ اختيار غير صحيح، حاولي مرة أخرى.")

        input("\nاضغطي Enter للمتابعة...")


if __name__ == "__main__":
    main()
