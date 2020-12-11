import vk_api
import json

def main():
    vk_session = vk_api.VkApi('liltechdude@gmail.com', "ВАШ ПАРОЛЬ ТУТА")
    vk_session.auth()
    vk = vk_session.get_api()
    tools = vk_api.VkTools(vk.session)
    posts = tools.get_all('wall.get', 1, {'domain': 'ryukishi07'}, negative_offset=False)
    with open('dest_file.json', 'w', encoding='utf8') as f:
        json.dump(posts, f, indent=4, sort_keys=True, ensure_ascii=False)
        
if __name__ == "__main__":
    main()
