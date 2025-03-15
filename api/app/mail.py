import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

async def send_email(receiver_email, content):
    # Thông tin tài khoản và email
    sender_email = "kienluong12345@gmail.com"         # Địa chỉ email của bạn
    password = "sqvgamkoyvojitil"                  # Mật khẩu (hoặc App Password)

    # Tạo đối tượng tin nhắn
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Tiêu đề email"

    # Nội dung email
    message.attach(MIMEText(content, "plain"))

    try:
        # Kết nối đến máy chủ SMTP của Gmail
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()            # Giới thiệu bản thân với máy chủ
        server.starttls()        # Kích hoạt mã hóa TLS
        server.login(sender_email, password)  # Đăng nhập với tài khoản Gmail

        # Gửi email
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email đã được gửi thành công!")
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")
    finally:
        server.quit()

