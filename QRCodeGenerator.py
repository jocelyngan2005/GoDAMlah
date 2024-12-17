import qrcode
import random
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import os
import threading

def generate_random_otp(length=6):
    # Generate a random OTP
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def generate_qr_code(data, file_path="qrcode.png"):
    # Generate a QR code and save it to the specified file path
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save(file_path)
    return file_path

def display_qr_code(file_path):
    # Display the QR code image in a tkinter window
    if not os.path.exists(file_path):
        print(f"Error: QR code file '{file_path}' not found.")
        return

    root = tk.Tk()
    root.title("QR Code")

    img = Image.open(file_path)
    qr_img = ImageTk.PhotoImage(img)
    label = Label(root, image=qr_img)
    label.pack()

    def close_window():
        root.destroy()

    # Close the window after 20 seconds (20000 milliseconds)
    root.after(20000, close_window)
    root.mainloop()


def verify_otp_with_timeout(original_otp, timeout=15):
    # Wait for user to input OTP with timeout, return True if correct, False if incorrect, and None if timeout
    otp_verified = False
    user_input = None

    def input_otp():
        nonlocal user_input, otp_verified
        user_input = input("Please enter the OTP: ").strip()
        if user_input == original_otp:
            otp_verified = True

    input_thread = threading.Thread(target=input_otp)
    input_thread.start()
    input_thread.join(timeout)

    if not otp_verified and user_input is None:
        print("Timeout!")
        return None  # Timeout
    elif not otp_verified:
        print("Invalid OTP!")
        return False  # Incorrect OTP
    return True  # Correct OTP

if __name__ == "__main__":
    try:
        while True:
            # Step 1: Generate the OTP and display the QR code
            otp = generate_random_otp(6)
            print(f"Generated OTP: {otp}")
            qr_code_file = generate_qr_code(otp)
            print("Scan the QR code to view the OTP.")
            display_qr_code(qr_code_file)

            attempts = 0
            max_attempts = 3

            while attempts < max_attempts:
                # Step 2: Verify the OTP with timeout
                result = verify_otp_with_timeout(otp, timeout=10)

                if result is None:  # Timeout
                    print("You need to regenerate the QR code due to timeout.")
                    break  # Exit the attempts loop to regenerate the QR code
                elif result is True:  # Correct OTP
                    print("OTP verified successfully! Proceeding...")
                    exit(0)
                else:  # Incorrect OTP
                    attempts += 1
                    if attempts < max_attempts:
                        print(f"You have {max_attempts - attempts} attempts remaining.")
                    else:
                        print("Maximum attempts reached. You need to regenerate the QR code.")

            # Step 3: Regenerate the QR code after timeout or 3 failed attempts
            user_command = input("Type 'generate' to create a new QR code or press Enter to quit: ").strip().lower()
            if user_command == "generate":
                continue  # Restart the loop to generate a new QR code
            elif user_command == "":
                print("Exiting the program...")
                break
            else:
                print("Invalid input. Exiting the program...")
                break

    except Exception as e:
        print(f"An error occurred: {e}")