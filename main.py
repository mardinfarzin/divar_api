import requests
from bs4 import BeautifulSoup

# تابع برای دریافت محتوای HTML صفحه
def get_page_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"خطا در ارسال درخواست به وب‌سایت: {e}")
        return None

# تابع برای دریافت اطلاعات از API دیوار
def get_api_data(token):
    if token:  # بررسی معتبر بودن token
        api_url = f"https://api.divar.ir/v5/posts/{token}"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            return data.get('data', {}).get('seo', {}).get('description', "توضیحات موجود نیست")
        except requests.exceptions.RequestException as e:
            print(f"خطا در دریافت اطلاعات از API: {e}")
            return "توضیحات موجود نیست"
    else:
        return "توکن نامعتبر است"

# تابع اصلی برای تجزیه و تحلیل HTML و دریافت اطلاعات آگهی‌ها
def divar_api(url):
    html_content = get_page_content(url)
    if not html_content:
        return []

    posts = []
    soup = BeautifulSoup(html_content, 'html.parser')

    # یافتن تگ‌های با کلاس kt-post-card--has-chat
    parents = soup.find_all(class_='kt-post-card--has-chat')

    for parent in parents:
        try:
            post = {}
            title = parent.find(class_="kt-post-card__title")
            post['title'] = title.text.strip() if title else "عنوان موجود نیست"

            thumbnail = parent.find(class_="kt-image-block__image")
            post['thumbnail'] = thumbnail.get("data-src") if thumbnail else "تصویر موجود نیست"

            location = parent.find(class_="kt-text-truncate")
            post['location'] = location.text.strip() if location else "موقعیت مکانی موجود نیست"

            token = parent.get("data-token")  # اطمینان حاصل کنید که token از تگ صحیح استخراج می‌شود
            post['token'] = token
            post['link'] = f"https://divar.ir/v/{token}" if token else "لینک موجود نیست"

            # دریافت توضیحات از API
            post['description'] = get_api_data(token)

            advs_info = parent.find_all(class_="kt-post-card__description")
            post["price"] = advs_info[0].text.strip() if advs_info else "قیمت موجود نیست"

            posts.append(post)
        except Exception as e:
            print(f"خطا در پردازش آگهی: {e}")
            continue

    return posts

url = 'https://divar.ir/s/iran/restaurant-equipment?goods-business-type=personal'
print(divar_api(url))
