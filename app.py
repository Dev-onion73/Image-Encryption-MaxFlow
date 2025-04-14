import streamlit as st
import os
import random
from PIL import Image

# ----- Styling -----
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}

    /* Console-like scrollable output box */
    .scrollable-output {
        height: 400px;
        overflow-y: auto;
        background-color: #1e1e1e;  /* Dark background */
        padding: 15px;
        border-radius: 8px;
        border: 2px solid #333;
        font-family: 'Courier New', monospace;
        font-size: 16px;
        color: #f1f1f1;  /* Light text color */
        line-height: 1.5;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.4);
    }

    /* For better readability: Add some subtle colors */
    .scrollable-output .info {
        color: #8dff00;  /* Console green */
    }
    
    .scrollable-output .error {
        color: #ff4d4d;  /* Red for errors */
    }
    
    .scrollable-output .debug {
        color: #a9a9a9;  /* Light gray for debug */
    }
    </style>
""", unsafe_allow_html=True)

# ----- Mock Functions -----
def encrypt(code):
    print(f"Encrypting image for {code}...")

def decrypt(code):
    # Dummy decrypt function
    # Replace this with your actual decryption logic
    # decrypted_image_path = encrypted_image_path.replace('encrypted', 'decrypted')
    # # Simulate decryption process (e.g., by modifying image)
    # os.rename(encrypted_image_path, decrypted_image_path)
    return f"data/{code}/{code}_output.png"

def visualize(code):
    print(f"Generating plot for {code}...")
    folder = f"data/{code}"
    plot_path = os.path.join(folder, f"{code}_plot.png")

    # Dummy plot
    img = Image.new("RGB", (400, 300), color=(200, 100, 150))
    img.save(plot_path)

    lines = [f"Line {i+1}: Visualization result..." for i in range(128)]

    # Save to log file
    with open(os.path.join(folder, f"{code}_log.txt"), "w") as f:
        f.write("\n".join(lines))

    return "\n".join(lines)

# ----- Save Function -----
def save_uploaded_image(uploaded_file):
    code = f"{random.randint(0, 9999):04}"
    folder = f"data/{code}"
    os.makedirs(folder, exist_ok=True)

    input_path = os.path.join(folder, f"{code}_input.png")
    image = Image.open(uploaded_file).convert("RGB")
    image.save(input_path)

    encrypt(code)
    vis_output = visualize(code)

    return code, vis_output

# ----- App UI -----
st.title("🖼️ Secure Image Exchange App")
tab1, tab2 = st.tabs(["📤 Send", "📥 Receive"])


# Send Tab - Upload Image and Encrypt
with tab1:
    st.header("Send Image for Encryption")

    uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Save the uploaded image temporarily
        input_image_path = "temp_input.png"
        with open(input_image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Call the encrypt function (it will process the image)
        encrypted_image = encrypt(input_image_path)  # Assuming encrypt() returns the processed image

        # Inform the user that the image has been encrypted
        st.info("🔒 The image has been successfully encrypted.")

        # Delete the input image file after encryption
        os.remove(input_image_path)
        st.info("The original input image has been deleted after encryption.")


# ----- Receive Tab -----
with tab2:
    st.header("Receive Output")

    st.markdown("Enter your **4-digit code**:")

    # Single input box for the 4-digit code
    code_input = st.text_input("Enter the 4-digit code", max_chars=4, key="code_input")

    if code_input.isdigit() and len(code_input) == 4:
        folder = f"data/{code_input}"
        encrypted_path = os.path.join(folder, f"{code_input}_input.png")  # Path to the encrypted image
        plot_path = os.path.join(folder, f"{code_input}_plot.png")  # Path to the plot
        log_path = os.path.join(folder, f"{code_input}_log.txt")

        # Check if the folder exists
        if os.path.isdir(folder):
            # Check if the encrypted image exists and decrypt it (in memory)
            if os.path.exists(encrypted_path):
                # Call the decrypt function and store the decrypted result in memory (not saving to file)
                decrypted_image = decrypt(code_input)  # Assuming decrypt() returns the image in memory
                st.image(decrypted_image, caption="Decrypted Image", use_container_width=True)
            else:
                st.warning("⚠️ Encrypted image not available.")
            
            # Check for the plot file and display it
            if os.path.exists(plot_path):
                st.image(plot_path, caption="Received Plot", use_container_width=True)
            else:
                st.warning("⚠️ Plot file not yet available.")
            
            # Display the log file (scrollable)
            if os.path.exists(log_path):
                with open(log_path, "r") as f:
                    log_text = f.read()
                st.markdown("### 📄 Visualization Output Log")
                st.markdown(f'<div class="scrollable-output">{log_text}</div>', unsafe_allow_html=True)
            else:
                st.info("ℹ️ No log file found.")
        else:
            st.error("❌ Invalid code. No such folder found.")
    else:
        st.warning("Please enter a valid 4-digit code.")