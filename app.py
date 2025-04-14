import os
import streamlit as st
import random

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

# Mock-up function to simulate encryption
def encrypt(input_image_path, code_input):
    # Create the directory for the given 4-digit code if it doesn't exist
    folder = f"data/{code_input}"
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Simulate encryption (moving file to the new directory)
    encrypted_image_path = os.path.join(folder, f"{code_input}_input.png")
    os.rename(input_image_path, encrypted_image_path)

    # Delete the original input image after encryption
    os.remove(input_image_path)
    print("Encrypted")

# Mock-up function to simulate decryption
def decrypt(code):
    return f"data/{code}/{code}_output.png"

def visualize(code):
    # print(f"Generating plot for {code}...")
    # folder = f"data/{code}"
    # plot_path = os.path.join(folder, f"{code}_plot.gif")

    # # Dummy plot
    # img = Image.new("RGB", (400, 300), color=(200, 100, 150))
    # img.save(plot_path)

    lines = [f"Line {i+1}: Visualization result..." for i in range(128)]

    # Save to log file
    with open(os.path.join(folder, f"{code}_log.txt"), "w") as f:
        f.write("\n".join(lines))

    return "\n".join(lines)

# ----- App UI -----
st.title("🖼️ Secure Image Exchange App")
tab1, tab2 = st.tabs(["📤 Send", "📥 Receive"])


# Send Tab - Upload Image and Encrypt
with tab1:
    st.header("Send Image for Encryption")

    uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Generate a unique 4-digit code for the file (simulating it here)
        code = str(random.randint(1000, 9999))

        # Display the code to the sender immediately
        st.write(f"Your unique 4-digit code: {code}")

        # Save the uploaded image temporarily
        folder = f"data/{code}"
        if not os.path.exists(folder):
            os.makedirs(folder)
        input_image_path = os.path.join(folder, f"{code}_input.png")
        with open(input_image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Encryption and Visualization
        encrypt(input_image_path, code)
        # Inform the user that the image has been encrypted
        st.info("🔒 The image has been successfully encrypted.")

        visualize(code)

        gif_path = f"data/1234/1234_plot.gif"
        log_path = f"data/{code}/{code}_log.txt"

        # Display the GIF (instead of plot)
        if os.path.exists(gif_path):
            st.image(gif_path, caption="Graph Animation", use_container_width=True)
        else:
            st.warning("⚠️ GIF file not yet available.")

        # Display log output in a scrollable box
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                log_text = f.read()
            st.markdown("### 📄 Visualization Output Log")
            st.markdown(f'<div class="scrollable-output">{log_text}</div>', unsafe_allow_html=True)
        else:
            st.info("ℹ️ No log file found.")

# Receiver Tab - Enter 4-digit Code, Decrypt and Display
with tab2:
    st.header("Receive Output")
    st.markdown("Enter your **4-digit code**:")

    # Single input box for the 4-digit code
    code_input = st.text_input("Enter the 4-digit code", max_chars=4, key="code_input")

    if code_input.isdigit() and len(code_input) == 4:
        folder = f"data/{code_input}"
        gif_path = os.path.join(folder, f"{code_input}_plot.gif")  # Path to the gif
        log_path = os.path.join(folder, f"{code_input}_log.txt")

        # Check if the folder exists
        if os.path.isdir(folder):
            # Display "Decrypting..." message
            decrypting_text = st.text("Decrypting... Please wait.")

            # Check if the encrypted image exists and decrypt it (in memory)
            if os.path.exists(folder):
                decrypted_image = decrypt(code_input)
                decrypting_text.text("Decryption Complete!")
                st.image(decrypted_image, caption="Decrypted Image", use_container_width=True)
            else:
                st.warning("⚠️ Invalid Code")
            
            # Check for the gif file and display it (for animation)
            if os.path.exists(gif_path):
                st.image(gif_path, caption="Received Animation", use_container_width=True)
            else:
                st.warning("⚠️ GIF file not yet available.")
            
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
