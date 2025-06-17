from fastapi import HTTPException, status


class HttpResponse:

  @staticmethod
  def not_found(message):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=message
    )
  
  @staticmethod
  def ok_message(message):
    return {"message": message}

