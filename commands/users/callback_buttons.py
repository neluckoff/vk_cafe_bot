from vkbottle.bot import Blueprint, Message
from vkbottle import GroupEventType, GroupTypes, OpenLinkEvent

vk = Blueprint("Callback user buttons")


@vk.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
async def product_handler(event: GroupTypes.MessageEvent):
    if event.object.payload["cmd"] == "cafe_menu":
        await vk.api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            peer_id=event.object.peer_id,
            user_id=event.object.user_id,
            event_data=OpenLinkEvent(link="https://vk.com/custom_bot?w=product-132641953_5352036%2Fquery").json()
        )
    elif event.object.payload["cmd"] == "reviews":
        await vk.api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            peer_id=event.object.peer_id,
            user_id=event.object.user_id,
            event_data=OpenLinkEvent(link="https://vk.com/uslugi-132641953?w=product-132641953_5352035%2Fquery").json()
        )
    elif event.object.payload["cmd"] == "sales":
        await vk.api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            peer_id=event.object.peer_id,
            user_id=event.object.user_id,
            event_data=OpenLinkEvent(link="https://vk.com/uslugi-132641953?w=product-132641953_5352038%2Fquery").json()
        )
