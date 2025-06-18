from fastapi import HTTPException, status


class HttpResponse:

  @staticmethod
  def ok_message(message):
    return {"message": message}

  @staticmethod
  def not_found(message):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=message
    )

  @staticmethod
  def unauthorized():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Ошибка проверки токена, возможно токен устарел или не прикреплен к запросу",
    )
  
  @staticmethod
  def forbidden():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="У вас нет прав на этот ресурс, проверьте корректность вашего токена",
    )
  
  @staticmethod
  def bad_request(message):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message,
    )
