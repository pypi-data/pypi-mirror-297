# Module note.py


bilibili_api.note

笔记相关


``` python
from bilibili_api import note
```

---

## class Note()

笔记相关




### async def add_coins()

(仅供公开笔记)

给笔记投币，目前只能投一个。



**Returns:** dict: 调用 API 返回的结果




### async def fetch_content()

获取并解析笔记内容

该返回不会返回任何值，调用该方法后请再调用 `self.markdown()` 或 `self.json()` 来获取你需要的值。



**Returns:** None



### def get_aid()

获取私有笔记对应视频 aid



**Returns:** int: aid




### async def get_all()

(仅供公开笔记)

一次性获取专栏尽可能详细数据，包括原始内容、标签、发布时间、标题、相关专栏推荐等



**Returns:** dict: 调用 API 返回的结果




### def get_cvid()

获取公开笔记 cvid



**Returns:** int: 公开笔记 cvid




### async def get_images()

获取笔记所有图片并转为 Picture 类



**Returns:** list: 图片信息




### async def get_images_raw_info()

获取笔记所有图片原始信息



**Returns:** list: 图片信息




### async def get_info()

获取笔记信息



**Returns:** dict: 笔记信息




### def get_note_id()

获取私有笔记 note_id



**Returns:** int: note_id




### async def get_private_note_info()

获取私有笔记信息。



**Returns:** dict: 调用 API 返回的结果。




### async def get_public_note_info()

获取公有笔记信息。



**Returns:** dict: 调用 API 返回的结果。




### def json()

转换为 JSON 数据

请先调用 fetch_content()



**Returns:** dict: JSON 数据




### def markdown()

转换为 Markdown

请先调用 fetch_content()



**Returns:** str: Markdown 内容




### async def set_favorite()

(仅供公开笔记)

设置专栏收藏状态


| name | type | description |
| - | - | - |
| status | Union[bool, None] | 收藏状态. Defaults to True |

**Returns:** dict: 调用 API 返回的结果




### async def set_like()

(仅供公开笔记)

设置专栏点赞状态


| name | type | description |
| - | - | - |
| status | Union[bool, None] | 点赞状态. Defaults to True |

**Returns:** dict: 调用 API 返回的结果




### def turn_to_article()

将笔记类转为专栏类。需要保证笔记是公开笔记。



**Returns:** Note: 专栏类




---

## class NoteType()

**Extend: enum.Enum**

笔记类型




