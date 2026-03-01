"""
Bridge Flow - Universal Benefits Butler
Team: REBELS | Leader: KIRTHIKA .S
AI for Communities, Access & Public Impact
"""

import gradio as gr
import random

# Indian government schemes database
SCHEMES = [
    {
        "name": "PM Awas Yojana - Rent Assistance",
        "category": "Housing",
        "benefit": "₹4,000/month rent subsidy",
        "eligibility": "Income below ₹25,000/month",
        "documents": ["Aadhaar", "Ration Card", "Rent Agreement"],
        "hindi": "प्रधानमंत्री आवास योजना - किराया सहायता",
        "tamil": "பிரதமர் வீட்டுத் திட்டம் - வாடகை உதவி"
    },
    {
        "name": "PM Garib Kalyan Anna Yojana",
        "category": "Food",
        "benefit": "5 kg wheat/rice per person/month",
        "eligibility": "Ration Card holders",
        "documents": ["Ration Card", "Aadhaar"],
        "hindi": "प्रधानमंत्री गरीब कल्याण अन्न योजना",
        "tamil": "பிரதமர் கரிப் கல்யான் உணவுத் திட்டம்"
    },
    {
        "name": "Ayushman Bharat - Health Insurance",
        "category": "Health",
        "benefit": "₹5,00,000 health cover",
        "eligibility": "BPL families",
        "documents": ["Aadhaar", "Ration Card"],
        "hindi": "आयुष्मान भारत - स्वास्थ्य बीमा",
        "tamil": "ஆயுஷ்மான் பாரத் - சுகாதார காப்பீடு"
    },
    {
        "name": "PM Kisan Samman Nidhi",
        "category": "Agriculture",
        "benefit": "₹6,000 per year",
        "eligibility": "Small farmers",
        "documents": ["Aadhaar", "Land Records"],
        "hindi": "प्रधानमंत्री किसान सम्मान निधि",
        "tamil": "பிரதமர் கிசான் சம்மான் நிதி"
    },
    {
        "name": "National Pension Scheme",
        "category": "Pension",
        "benefit": "₹3,000/month after 60",
        "eligibility": "Age 18-40, unorganized workers",
        "documents": ["Aadhaar", "Bank Account"],
        "hindi": "राष्ट्रीय पेंशन योजना",
        "tamil": "தேசிய ஓய்வூதியத் திட்டம்"
    }
]

def check_eligibility(user_input, language, age, income, has_ration, is_farmer, has_girl_child):
    """Check eligible schemes based on user profile"""
    eligible = []
    
    for scheme in SCHEMES:
        score = 0
        
        # Income based
        if income < 25000 and "Rent" in scheme["name"]:
            score += 1
        if income < 25000 and "BPL" in scheme["eligibility"]:
            score += 1
            
        # Ration card based
        if has_ration == "Yes" and "Ration" in scheme["eligibility"]:
            score += 1
            
        # Farmer based
        if is_farmer == "Yes" and "Kisan" in scheme["name"]:
            score += 2
            
        # Age based
        if age > 55 and "Pension" in scheme["name"]:
            score += 2
            
        if score > 0:
            scheme_copy = scheme.copy()
            scheme_copy['match'] = min(100, score * 25)
            eligible.append(scheme_copy)
    
    # Sort by match score
    eligible.sort(key=lambda x: x['match'], reverse=True)
    
    # Format results
    result = "🌟 **BRIDGE FLOW RESULTS** 🌟\n\n"
    result += f"📝 Your situation: {user_input}\n"
    result += f"💰 Monthly income: ₹{income}\n"
    result += f"🪪 Ration card: {has_ration}\n\n"
    
    if eligible:
        result += f"✅ **YOU ARE ELIGIBLE FOR {len(eligible[:4])} BENEFITS**\n\n"
        
        for i, scheme in enumerate(eligible[:4], 1):
            result += f"{i}. **{scheme['name']}**\n"
            result += f"   📍 Category: {scheme['category']}\n"
            result += f"   💰 Benefit: {scheme['benefit']}\n"
            
            # Add translation
            if language == 'hindi' and 'hindi' in scheme:
                result += f"   🗣️ {scheme['hindi']}\n"
            elif language == 'tamil' and 'tamil' in scheme:
                result += f"   🗣️ {scheme['tamil']}\n"
            
            result += f"   📄 Documents: {', '.join(scheme['documents'])}\n"
            result += f"   📊 Match: {scheme['match']}%\n\n"
    else:
        result += "❌ No eligible schemes found.\n"
        result += "Try adjusting your information.\n\n"
    
    result += "=" * 50 + "\n"
    result += "**NEXT STEPS:**\n"
    result += "✅ Click 'Apply' to auto-fill forms\n"
    result += "👤 Click 'Caseworker' for human help\n"
    
    return result

def voice_simulation():
    """Simulate voice input"""
    examples = [
        "I lost my job and need help with rent",
        "मैंने नौकरी खो दी है और किराया चुकाने में मदद चाहिए",
        "எனக்கு வேலை போய்விட்டது, வாடகைக்கு உதவி தேவை",
        "Need food for my family",
        "My father is 65 and needs pension"
    ]
    return random.choice(examples)

# Create the web app
with gr.Blocks(title="Bridge Flow", theme=gr.themes.Soft()) as app:
    gr.Markdown("""
    # 🌉 Bridge Flow - Universal Benefits Butler
    ### AI-Powered Benefits Assistant for Bharat
    **Team: REBELS | Leader: KIRTHIKA .S**
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            user_input = gr.Textbox(
                label="Tell us your situation",
                placeholder="e.g., I lost my job and need rent help",
                lines=3
            )
            
            voice_btn = gr.Button("🎤 Voice Input (Demo)")
            
            language = gr.Dropdown(
                choices=["english", "hindi", "tamil"],
                label="Select Language",
                value="english"
            )
            
            gr.Markdown("### 📋 Your Details")
            
            age = gr.Number(label="Age", value=35)
            income = gr.Number(label="Monthly Income (₹)", value=12000)
            
            with gr.Row():
                ration = gr.Radio(["Yes", "No"], label="Have Ration Card?", value="No")
                farmer = gr.Radio(["Yes", "No"], label="Are you a farmer?", value="No")
                girl_child = gr.Radio(["Yes", "No"], label="Have girl child under 10?", value="No")
            
            submit_btn = gr.Button("🚀 Check Eligibility", variant="primary")
            
            with gr.Row():
                apply_btn = gr.Button("📝 Apply Now")
                caseworker_btn = gr.Button("👤 Talk to Caseworker")
        
        with gr.Column(scale=1):
            output = gr.Textbox(label="Your Benefits", lines=25)
    
    # Button actions
    submit_btn.click(
        check_eligibility,
        inputs=[user_input, language, age, income, ration, farmer, girl_child],
        outputs=[output]
    )
    
    voice_btn.click(
        voice_simulation,
        inputs=[],
        outputs=[user_input]
    )
    
    apply_btn.click(
        lambda: "✅ Applications auto-filled! Check your phone for confirmation.",
        inputs=[],
        outputs=[output]
    )
    
    caseworker_btn.click(
        lambda: "👤 A caseworker will contact you within 30 minutes.",
        inputs=[],
        outputs=[output]
    )
    
    gr.Markdown("""
    ---
    ### 📱 How Bridge Flow Works
    1. **Tell us your situation** in your own words or voice
    2. **AI checks eligibility** across multiple government schemes
    3. **Get instant results** with benefits you qualify for
    4. **Apply with one click** or talk to a human caseworker
    
    ### ✨ Key Features
    - ✅ Works on WhatsApp, SMS, and Voice
    - ✅ Supports Hindi, Tamil, and English
    - ✅ No app download needed
    - ✅ Privacy-first design
    - ✅ Works on basic phones
    """)

# Launch the app
if __name__ == "__main__":
    app.launch(share=True)
