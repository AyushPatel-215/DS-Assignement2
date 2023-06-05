import aiohttp_jinja2
import os
import zipfile
import jinja2
from aiohttp import web


async def handle(request):
    response = aiohttp_jinja2.render_template("index.html", request, context={})
    return response


async def handle1(request):
    data = await request.post()
    zip_file = data['filename'].file
    with zipfile.ZipFile(zip_file, 'r') as f:
        extracted_files = f.namelist()
        f.extractall(os.path.join(os.getcwd(), 'Downloaded Files'))
        file_name_dict = {'Name': extracted_files}

        response = aiohttp_jinja2.render_template("list.html", request, context=file_name_dict)
        return response


async def handle2(request):
    name = request.match_info.get('name')
    response = web.FileResponse(path=os.path.join(os.getcwd(), "Downloaded Files", name))
    return response


if __name__ == '__main__':
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('Templates'))
    app.router.add_get('/', handle)
    app.router.add_post('/Filename', handle1)
    app.router.add_get('/Files/{name}', handle2)
    web.run_app(app)
