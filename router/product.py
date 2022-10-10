from typing import Optional, List
from fastapi import APIRouter, Header, Cookie, Form
from fastapi.responses import Response, HTMLResponse, PlainTextResponse
from custom_log import log
import time

router = APIRouter(
    prefix='/product',
    tags=['product']
)

products = ['watch', 'camera', 'phone']

@router.post('new')
def create_product(name: str = Form(...)):
    products.append(name)
    return products


async def time_consuming_functionality():
    time.sleep(5)
    return 'ok'


@router.get('/all')
async def get_all_product():
    await time_consuming_functionality()
    log("myAPI", "Call to get all products")
    # return products
    data = " ".join(products)
    respone = Response(content=data, media_type="text/plain")
    respone.set_cookie(key='test_cookie', value='test_cookie_value')
    return respone


@router.get('/withheader')
def get_products(
        response: Response,
        custom_header: Optional[List[str]] = Header(None),
        test_cookie: Optional[str] = Cookie(None)
):
    if custom_header:
        response.headers['custom_response_header'] = ', '.join(custom_header)
    return {
        'data': products,
        'custome_header': custom_header,
        'my_cookie': test_cookie
    }


@router.get('/{id}', responses={
    200: {
        "content": {
            "text/html": {
                "example": "<div>Product</div>"
            }
        },
        "description": "Returns the html for an object"
    },
    404: {
        "content": {
            "text/plain":  {
                "example": "Product not avaiable"
            }
        },
        "description": "Clear text error message"

    }
})
def get_product(id: int):
    if id > len(products):
        out = 'Product not avaiable'
        return PlainTextResponse(content=out, media_type="text/plain")
    else:
        product = products[id]
        out = f"""
        <head>
            <style>
            .product {{
                width: 500px;
                height: 30px;
                border: 2px inset green;
                background-color: lightblue;
                texk=align: center;
            }}
            </style>
        </head>
        <div class="product">{product}</div>
        """
        return HTMLResponse(content=out, media_type="text/html")
