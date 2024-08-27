import streamlit as st
import os
from groq import Groq


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)



# -- page config
st.set_page_config(
    page_title="TailorMail",
    page_icon="📧",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# -- hiding the sidebar
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)


# variable to check button status
if 'access' not in st.session_state:
    st.session_state.access = False

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []


system_prompt = {"role": "system", 
                     "content": "You are an expert at writing personalized emails. Your task is to write a personalized email in a mail format given some details of the email like recipient details, sender details, reason of email and some other attributes of mail. And make changes based on user's follow up requests."}



# welcome page
def welcome_page():

    # -- page title
    st.markdown(
        "<h1 style='text-align: center;'>Welcome to TailorMail📧</h1>", unsafe_allow_html=True
    )
    st.markdown(
        "<h5 style='text-align: center;'>Personalize Your Emails with Ease</h5>",
        unsafe_allow_html=True,
    )

    # -- adding space b/w texts
    st.title("\n\n")

    button_style = """
    <style>
    .stButton>button{
        width: 180px;
        height: 80px;
        font-size: 100px;
    }
    </style>"""

    

    cols = st.columns((1,2,1))
    
    with cols[1]: 

        access_button = st.button("Access the tool", type = "primary", use_container_width=True)

        if access_button:
            st.session_state['access'] = True
            st.rerun()  # This can be replaced with navigation to the main tool interface



def generate_user_prompt(recipient_name, recipient_role, company_name, sender_name, sender_role, sender_contact, 
                    sender_company, email_reason, specific_details, language, tone_style, cta_outcome, 
                    attachment_info, additional_instructions):
    
    prompt = f"""Instructions to draft the mail: 
    1. Understand the details about recipient, sender and other attributes of email like reason, tone, language, etc.
    2. The subject of the mail will not be provided to you, so once you understand the reason and other details about the mail, create a good subject for the mail that meets the user requirements and is in aligned with the details mentioned.
    3. The output returned need to be of the email format and not as one big long paragraph.
    4. Do add greetings based on the type of the mail.

    IMPORTANT: User might not provide us with some these details : recipient_role, company_name, sender_role, sender_contact, sender_company, specific_details, cta_outcome, attachment_info, additional_instructions. So in that case don't interpret things and add up on your own. You need to generate content based on the content user has provided and ignore the fields which user has left blank (empty string).
    
    Also, don't show variable names in the response, use the names and details which are provided and leave the ones which are blank or empty strings.
    Make sure to not add any extra commentary in the output other than the complete mail. And avoid using special symbols like * etc on the places where its not required.

    Here are the details of the email provided by the user. Use these details to draft a mail, remember some of these could be empty strings: 

    Recipient Name : {recipient_name},

    Recipient Role: {recipient_role},

    Recipient Company Name: {company_name}, 

    Sender Name: {sender_name}, 

    Sender Role: {sender_role}, 

    Sender Contact: {sender_contact}, 

    Sender Company: {sender_company}, 

    Reason of writing the mail: {email_reason}, 

    Specific details about the mail, if any: {specific_details}, 

    Formality Type: {language}, 

    Tone of the mail: {tone_style}, 

    Call to action, if any: {cta_outcome}, 

    Information about the file or document attached, if any: {attachment_info}, 

    These are some special instructions from the user that we need to consider while drafting the mail: {additional_instructions}"""

    return prompt


def generate_response(user_prompt, model, temperature, tokens):
    messages = st.session_state.conversation_history + [{"role": "user", "content": user_prompt}]
    
    if model=='Mistral':
        model = 'mixtral-8x7b-32768'
    else:
        model = 'llama-3.1-8b-instant'

    chat_completion = client.chat.completions.create(
        messages=messages,
        model= model,
        temperature = temperature, 
        max_tokens = tokens
    )
    
    response = chat_completion.choices[0].message.content
    
    # Append the assistant's response to the conversation history
    st.session_state.conversation_history.append({"role": "assistant", "content": response})
    
    return response



def run_email_tool(st):
    
    # Apply custom CSS to style the Streamlit app
    st.markdown(
        """
        <style>
        .stTextInput > div > input {
            color: #000000;
            background-color: #f2f2f2;
            border-radius: 5px;
            border: 1px solid #d9d9d9;
        }
        .stTextArea > div > textarea {
            color: #000000;
            background-color: #f2f2f2;
            border-radius: 5px;
            border: 1px solid #d9d9d9;
        }
        .stRadio > div > div > label > div {
            color: #688da2;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 24px;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # UI Title
    st.markdown("<h1 style='color: #2180b9; text-align: center;'>TailorMail📧</h1>", unsafe_allow_html=True)

    # Section 1: Recipient Information
    st.markdown("<h2 style='color: #688da2;'>Recipient Information</h2>", unsafe_allow_html=True)

    # Recipient's Name Field
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0px; padding-bottom: 0px">
            <span style="color: #c94d4d; font-weight: bold;">Recipient's Name</span>
            <span style="color: grey; font-size: 0.9em;">(Required)</span>
        </div>
        """, unsafe_allow_html=True)
    recipient_name = st.text_input("", placeholder="e.g., John Doe", key="recipient_name", label_visibility="collapsed")

    # Add a small margin between the input field and the next heading
    st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

    # Recipient's Job Title/Role Field
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0px; padding-bottom: 0px">
            <span style="font-weight: bold;">Recipient's Job Title/Role</span>
            <span style="color: grey; font-size: 0.9em;">(Optional)</span>
        </div>
        """, unsafe_allow_html=True)
    recipient_role = st.text_input("", placeholder="e.g., Marketing Manager", key="recipient_role", label_visibility="collapsed")


    # Company Name Field
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0px; padding-bottom: 0px">
            <span style="font-weight: bold;">Company Name</span>
            <span style="color: grey; font-size: 0.9em;">(Optional)</span>
        </div>
        """, unsafe_allow_html=True)
    company_name = st.text_input("", placeholder="e.g., ABC Corporation", label_visibility="collapsed")

    # Section 2: Sender Information
    st.markdown("<h2 style='color: #688da2;'>Sender Information</h2>", unsafe_allow_html=True)

    # Sender's Name Field
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0px; padding-bottom: 0px">
            <span style="color: #c94d4d; font-weight: bold;">Sender's Name</span>
            <span style="color: grey; font-size: 0.9em;">(Required)</span>
        </div>
        """, unsafe_allow_html=True)
    sender_name = st.text_input("", placeholder="e.g., Jane Smith", label_visibility="collapsed")

    # Sender's Job Title Field
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0px; padding-bottom: 0px">
            <span style="font-weight: bold;">Sender's Job Title</span>
            <span style="color: grey; font-size: 0.9em;">(Optional)</span>
        </div>
        """, unsafe_allow_html=True)
    sender_role = st.text_input("", placeholder="e.g., Project Lead", label_visibility="collapsed")

    # Sender's Contact Information Field
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0px; padding-bottom: 0px">
            <span style="font-weight: bold;">Sender's Contact Information</span>
            <span style="color: grey; font-size: 0.9em;">(Optional)</span>
        </div>
        """, unsafe_allow_html=True)
    sender_contact = st.text_input("", placeholder="Enter your mail or mobile number", label_visibility="collapsed")

    # Sender's Company Name/Organization Field
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0px; padding-bottom: 0px">
            <span style="font-weight: bold;">Company Name/Organization</span>
            <span style="color: grey; font-size: 0.9em;">(Optional)</span>
        </div>
        """, unsafe_allow_html=True)
    sender_company = st.text_input("", placeholder="e.g., XYZ Ltd.", label_visibility="collapsed")

    # Section 3: Purpose of the Email
    st.markdown("<h2 style='color: #688da2;'>Purpose of the Email</h2>", unsafe_allow_html=True)

    # Reason for the Email Field
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0px; padding-bottom: 0px">
            <span style="color: #c94d4d; font-weight: bold;">Reason for the Email</span>
            <span style="color: grey; font-size: 0.9em;">(Required)</span>
        </div>
        """, unsafe_allow_html=True)
    email_reason = st.text_area("", placeholder="e.g., I want to discuss the project updates", label_visibility="collapsed")

    # Specific Details Field
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0px; padding-bottom: 0px">
            <span style="font-weight: bold;">Specific Details</span>
            <span style="color: grey; font-size: 0.9em;">(Optional)</span>
        </div>
        """, unsafe_allow_html=True)
    specific_details = st.text_area("", placeholder="Enter any specific details that you would like to mention e.g., Provide an update on the project status...", label_visibility="collapsed")

    # Section 4: Tone of the Email
    st.markdown("<h2 style='color: #688da2;'>Tone of the Email</h2>", unsafe_allow_html=True)

    # CSS to make radio button options appear side by side
    st.markdown(
    """
    <style>
    .stRadio > div {
    flex-direction: row;
    }
    """,
        unsafe_allow_html=True,
    )

    language = st.radio("Language", options=["Formal", "Informal"], index=0)
    tone_style = st.radio("Tone", options=["Friendly", "Professional", "Urgent"], index=1)

    # Section 5: Call to Action (CTA)
    st.markdown("<h2 style='color: #688da2;'>Call to Action (CTA)</h2>", unsafe_allow_html=True)

    # Desired Outcome Field
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0px; padding-bottom: 0px">
            <span style="font-weight: bold;">Desired Outcome</span>
            <span style="color: grey; font-size: 0.9em;">(Optional)</span>
        </div>
        """, unsafe_allow_html=True)
    cta_outcome = st.text_input("", placeholder="e.g., Schedule a meeting for next week", label_visibility="collapsed")

    # Section 7: Attachments
    st.markdown("<h2 style='color: #688da2;'>Attachments</h2>", unsafe_allow_html=True)

    # Attachment Information Field
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0px; padding-bottom: 0px">
            <span style="font-weight: bold;">Attachment Information</span>
            <span style="color: grey; font-size: 0.9em;">(Optional)</span>
        </div>
        """, unsafe_allow_html=True)
    attachment_info = st.text_area("", placeholder="e.g., I have attached the documentation that explains the workflow...", label_visibility="collapsed")

    # Section 8: Additional Instructions to the Bot
    st.markdown("<h2 style='color: #688da2;'>Additional Instructions to the Bot</h2>", unsafe_allow_html=True)

    # Additional Instructions Field
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0px; padding-bottom: 0px">
            <span style="font-weight: bold;">Additional Instructions</span>
            <span style="color: grey; font-size: 0.9em;">(Optional)</span>
        </div>
        """, unsafe_allow_html=True)
    additional_instructions = st.text_area("", placeholder="e.g., I want the email to be written in 200 words, Add a very catchy subject for this mail,...", label_visibility="collapsed")


    # Section 9: Model Parameters 
    st.markdown("<h2 style='color: #688da2;'>Model Parameters</h2>", unsafe_allow_html=True)
    
    model = st.radio("Select a Model", options=["Llama 3.1", "Mixtral"], index=0)

    temperature = st.slider('Temperature (higher value more random output, lesser value more stable output)', 0.0, 2.0, step=0.01, value = 1.0)
    
    tokens = st.slider('Max words:', 0, 32000, step=20, value = 1024)

    st.markdown("\n\n")

    # Submit Button
    if st.button("Generate Mail", use_container_width=True):
        if not recipient_name:
            st.error("Please provide the recipient's name.")
        elif not sender_name:
            st.error("Please provide the sender's name.")
        elif not email_reason:
            st.error("Please provide the reason for the email.")
        else:
            with st.spinner(text="Generating mail..."):
                
                # Process the input data and generate the email content
                email_prompt = generate_user_prompt(recipient_name, recipient_role, company_name, sender_name, sender_role, 
                                            sender_contact, sender_company, email_reason, specific_details, 
                                            language, tone_style, cta_outcome, attachment_info, additional_instructions)
                
                # Generate and display the email content
                response = generate_response(email_prompt, model, temperature, tokens)
                st.markdown("<h3 style='color: #2180b9;'>Generated Email</h3>", unsafe_allow_html=True)
                st.text_area(label="", value=response, height=400)



if not st.session_state['access']:
    welcome_page()
else:
    run_email_tool(st)
