import EmailUtil
from FbUtil import UtilFacebook

commentsNeedingHelp =  UtilFacebook().getCommentsNeedingHelp()
print(EmailUtil.send(emailTo="email",subject="subject", commentData=commentsNeedingHelp))








