from fastapi import HTTPException, status
import httpx


class APIService:
    @classmethod
    async def get_posts(cls, client: httpx.AsyncClient):
        response = await client.get("https://jsonplaceholder.typicode.com/posts")
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not get data from API",
            )
        return response.json()
