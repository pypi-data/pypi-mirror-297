# UCONRA
## An application security hasher, tokenization and SMTP creator

uconra is a simple appplication Authentication security 
password hasher and basic tokenization and smtp creator for
basic python, flask or django applications

### Installation
"""

    pip install uconra
"""

# Different usages for different use cases.

### Usage for password hashing and email validation

"""

    from uconra.register import Register

    pass_word = 'enter_your_password'
    user_email = 'cody@gmail.com'

    email = str(register.userEmail(user_email))

    password = register.userPassword(pass_word)

    print(password)

"""

###  Usage for creating basic j_wt token
""" 
    
    from uconra.j_wt import JWT

    token = JWT()

    login_token = token.generate_jwt_token('cody@gmail.com', key='3uiojjkskdpeisjdjfl')

    print(f"encoded jwt token : {login_token}")

    decode_login_token = token.decode_jwt_token(login_token)

    print(decode_login_token['email'])

    print(f"decoded jwt token : {decode_login_token}")
"""

### smtp basic usage setup

"""
    
    
    from uconra.smtp_mail import SMTP_Mail

    confirm_message = MailMessage()
    """
    app_pw = 'hjdj j3l2 guess whaid'
    myMail = 'cody@gmail.com'
    mail_server = 'smtp.gmail.com:587'
    ehlo = 'Gmail'
    message = 'Here goes your message'
    user = 'user@gmail.com'
    OTP = 1324
    """

    sendMail = SMTP_Mail(
    appKey=app_pw, userMail=email,
    senderMail=myMail, serverEhlo=ehlo,
    smtpServer=mail_server,
    subject='TEST SUBJECT', userName=username,
    message=confirm_message.confirm_message(token=login_token, otp=OTP),
                    )
   
    sendMail.sendMail()

"""

### Mail message for the above smtp usage

"""

    from uconra.email_message import MailMessage

    message = MailMessage()

    print(message.confirm_message(token=7890))
"""



