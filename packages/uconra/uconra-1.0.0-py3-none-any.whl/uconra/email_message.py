import requests



class MailMessage:
    def __init__(self, ):
        pass

    def confirm_message(self, user=None, otp=None, content=None, url=None, token=None, *args):
        self.user = user
        self.content = content
        self.message = message = f""" <!DOCTYPE html>
<html lang="en">
<head>
<title>CSS Website Layout</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>

<div class="header">
  <h1>Confirm Email </h1>
</div>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>


<div style="width:100%; background-color:deeppink; color:white;">

    <div style=" margin: auto; width: 50%;">
  
      <h1>  Thank you For Signing Up with Fruutty </h1>
      <p> Please click the link to get started </p>
      
    </div>  
      
      
      
  
</div>

</body>
</html>

<div style="width:100%; background-color:yellow;color:black">

    <div style=" margin: auto; width: 50%;">

         <p> Click to confirm email   </p> </br> </br>
         
         <a href="http://127.0.0.1:5000/jwt-confirm/{token}  "> <button style=" width: 50%; color:deeppink; "> confirm </button>  </a> </br>
         
         <h3> or copy and type this otp code to confirm <h2> {otp} </h2> </h3> </br> 
         <h3> as an alternative </h3>
         
    </div>     
         
 </div>
 
 
 
 <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>


<div style=" width: 100%; background-color: deeppink; color: white" >

    <div style=" margin: auto; width: 50%;">
  
  <h1>  Fruutty also known as (FTVS) </h1>
  <h5> Use and trade resposibly  </h5>
   </div>
  
  
</div>

</body>
</html>
 
</body>
</html>

"""

        return self.message

    def reset_message(self, user=None, otp=None, content=None, url=None, token=None, *args):
        self.reset_message = reset_message = f""" <!DOCTYPE html>
<html lang="en">
<head>
<title>CSS Website Layout</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>

<div class="header">
  <h1> Reset Password </h1>
</div>
 
 
  <h3> copy and type this otp code to reset <h2> {otp} </h2> </h3> </br> 
 <h3> as an alternative </h3>
</body>
</html>

"""
        return self.reset_message

    def approve_message(self, user=None, otp=None, content=None, url=None, token=None, *args):
        self.approve_message = reset_message = f""" <!DOCTYPE html>
    <html lang="en">
    <head>
    <title>CSS Website Layout</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>

    <div class="header">
      <h1> Application Approved </h1>
    </div>
    <p> Click the link to create your employment password --> : http://127.0.0.1:5000/employment-id/{token}  </p> </br>


        <p>{content} </p>
    </body>
    </html>

    """
        return self.approve_message


if __name__ == '__main__':
    message = MailMessage()
    print(message.confirm_message(token=7890))

