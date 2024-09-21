import json
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pyroherd
from pyroherd import Client
from pyroherd import ContinuePropagation
from pyroherd.raw.base import InputPeer
from pyroherd.raw.functions.channels import GetFullChannel
from pyroherd.raw.functions.messages import GetFullChat
from pyroherd.raw.functions.phone import CreateGroupCall
from pyroherd.raw.functions.phone import EditGroupCallParticipant
from pyroherd.raw.functions.phone import GetGroupCall
from pyroherd.raw.functions.phone import GetGroupParticipants
from pyroherd.raw.functions.phone import JoinGroupCall
from pyroherd.raw.functions.phone import LeaveGroupCall
from pyroherd.raw.types import Channel
from pyroherd.raw.types import ChannelForbidden
from pyroherd.raw.types import Chat
from pyroherd.raw.types import ChatForbidden
from pyroherd.raw.types import DataJSON
from pyroherd.raw.types import GroupCall
from pyroherd.raw.types import GroupCallDiscarded
from pyroherd.raw.types import InputChannel
from pyroherd.raw.types import InputGroupCall
from pyroherd.raw.types import InputPeerChannel
from pyroherd.raw.types import MessageActionChatDeleteUser
from pyroherd.raw.types import MessageActionInviteToGroupCall
from pyroherd.raw.types import MessageService
from pyroherd.raw.types import PeerChat
from pyroherd.raw.types import UpdateChannel
from pyroherd.raw.types import UpdateGroupCall
from pyroherd.raw.types import UpdateGroupCallConnection
from pyroherd.raw.types import UpdateGroupCallParticipants
from pyroherd.raw.types import UpdateNewChannelMessage
from pyroherd.raw.types import UpdateNewMessage
from pyroherd.raw.types import Updates

from ..types import GroupCallParticipant
from ..version_manager import VersionManager
from .bridged_client import BridgedClient
from .client_cache import ClientCache


class PyroherdClient(BridgedClient):
    def __init__(
            self,
            cache_duration: int,
            client: Client,
    ):
        self._app: Client = client
        if VersionManager.version_tuple(
                pyroherd.__version__,
        ) > VersionManager.version_tuple(
            '0.0.10',
        ):
            self._app.send = self._app.invoke
        self._cache: ClientCache = ClientCache(
            cache_duration,
            self,
        )

        @self._app.on_raw_update()
        async def on_update(_, update, __, data2):
            if isinstance(
                    update,
                    UpdateGroupCallParticipants,
            ):
                participants = update.participants
                for participant in participants:
                    result = self._cache.set_participants_cache(
                        update.call.id,
                        self.parse_participant(participant),
                    )
                    if result is not None:
                        if 'PARTICIPANTS_HANDLER' in self.HANDLERS_LIST:
                            await self._propagate(
                                'PARTICIPANTS_HANDLER',
                                self._cache.get_chat_id(update.call.id),
                                result,
                                participant.just_joined,
                                participant.left,
                            )
            if isinstance(
                    update,
                    UpdateGroupCall,
            ):
                chat_id = self.chat_id(data2[update.chat_id])
                if isinstance(
                        update.call,
                        GroupCall,
                ):
                    if update.call.schedule_date is None:
                        self._cache.set_cache(
                            chat_id,
                            InputGroupCall(
                                access_hash=update.call.access_hash,
                                id=update.call.id,
                            ),
                        )
                if isinstance(
                        update.call,
                        GroupCallDiscarded,
                ):
                    self._cache.drop_cache(chat_id)
                    if 'CLOSED_HANDLER' in self.HANDLERS_LIST:
                        await self._propagate(
                            'CLOSED_HANDLER',
                            chat_id,
                        )
            if isinstance(
                    update,
                    UpdateChannel,
            ):
                chat_id = self.chat_id(update)
                if len(data2) > 0:
                    if isinstance(
                            data2[update.channel_id],
                            ChannelForbidden,
                    ):
                        self._cache.drop_cache(chat_id)
                        if 'KICK_HANDLER' in self.HANDLERS_LIST:
                            await self._propagate(
                                'KICK_HANDLER',
                                chat_id,
                            )
            if isinstance(
                    update,
                    UpdateNewChannelMessage,
            ) or isinstance(
                update,
                UpdateNewMessage,
            ):
                if isinstance(
                        update.message,
                        MessageService,
                ):
                    if isinstance(
                            update.message.action,
                            MessageActionInviteToGroupCall,
                    ):
                        if 'INVITE_HANDLER' in self.HANDLERS_LIST:
                            await self._propagate(
                                'INVITE_HANDLER',
                                update.message.action,
                            )
                    if isinstance(
                            update.message.action,
                            MessageActionChatDeleteUser,
                    ):
                        if isinstance(
                                update.message.peer_id,
                                PeerChat,
                        ):
                            chat_id = self.chat_id(update.message.peer_id)
                            if isinstance(
                                    data2[update.message.peer_id.chat_id],
                                    ChatForbidden,
                            ):
                                self._cache.drop_cache(chat_id)
                                if 'KICK_HANDLER' in self.HANDLERS_LIST:
                                    await self._propagate(
                                        'KICK_HANDLER',
                                        chat_id,
                                    )
            if isinstance(
                    data2,
                    Dict,
            ):
                for group_id in data2:
                    if isinstance(
                            update,
                            UpdateNewChannelMessage,
                    ) or isinstance(
                        update,
                        UpdateNewMessage,
                    ):
                        if isinstance(
                                update.message,
                                MessageService,
                        ):
                            if isinstance(
                                    data2[group_id],
                                    Channel,
                            ) or isinstance(
                                data2[group_id],
                                Chat,
                            ):
                                chat_id = self.chat_id(data2[group_id])
                                if data2[group_id].left:
                                    self._cache.drop_cache(
                                        chat_id,
                                    )
                                    if 'LEFT_HANDLER' in self.HANDLERS_LIST:
                                        await self._propagate(
                                            'LEFT_HANDLER',
                                            chat_id,
                                        )
            raise ContinuePropagation()

    async def get_call(
            self,
            chat_id: int,
    ) -> Optional[InputGroupCall]:
        chat = await self._app.resolve_peer(chat_id)
        if isinstance(chat, InputPeerChannel):
            input_call = (
                await self._app.send(
                    GetFullChannel(
                        channel=InputChannel(
                            channel_id=chat.channel_id,
                            access_hash=chat.access_hash,
                        ),
                    ),
                )
            ).full_chat.call
        else:
            input_call = (
                await self._app.send(
                    GetFullChat(chat_id=chat.chat_id),
                )
            ).full_chat.call

        if input_call is not None:
            call: GroupCall = (
                await self._app.send(
                    GetGroupCall(
                        call=input_call,
                        limit=-1,
                    ),
                )
            ).call

            if call.schedule_date is not None:
                return None

        return input_call

    async def get_group_call_participants(
            self,
            chat_id: int,
    ):
        return await self._cache.get_participant_list(
            chat_id,
        )

    async def get_participants(
            self,
            input_call: InputGroupCall,
    ) -> List[GroupCallParticipant]:
        return [
            self.parse_participant(participant)
            for participant in (
                await self._app.send(
                    GetGroupParticipants(
                        call=input_call,
                        ids=[],
                        sources=[],
                        offset='',
                        limit=500,
                    ),
                )
            ).participants
        ]

    async def join_group_call(
            self,
            chat_id: int,
            json_join: str,
            invite_hash: str,
            have_video: bool,
            join_as: InputPeer,
    ) -> str:
        chat_call = await self._cache.get_full_chat(chat_id)
        if chat_call is not None:
            result: Updates = await self._app.send(
                JoinGroupCall(
                    call=chat_call,
                    params=DataJSON(data=json_join),
                    muted=False,
                    join_as=join_as,
                    video_stopped=have_video,
                    invite_hash=invite_hash,
                ),
            )
            for update in result.updates:
                if isinstance(
                        update,
                        UpdateGroupCallParticipants,
                ):
                    participants = update.participants
                    for participant in participants:
                        self._cache.set_participants_cache(
                            update.call.id,
                            self.parse_participant(participant),
                        )
                if isinstance(update, UpdateGroupCallConnection):
                    return update.params.data

        return json.dumps({'transport': None})

    async def create_group_call(
            self,
            chat_id: int,
    ):
        result: Updates = await self._app.send(
            CreateGroupCall(
                peer=await self.resolve_peer(chat_id),
                random_id=self.rnd_id(),
            ),
        )
        for update in result.updates:
            if isinstance(
                update,
                UpdateGroupCall,
            ):
                if isinstance(
                    update.call,
                    GroupCall,
                ):
                    if update.call.schedule_date is None:
                        self._cache.set_cache(
                            chat_id,
                            InputGroupCall(
                                access_hash=update.call.access_hash,
                                id=update.call.id,
                            ),
                        )

    async def leave_group_call(
            self,
            chat_id: int,
    ):
        chat_call = await self._cache.get_full_chat(chat_id)
        if chat_call is not None:
            await self._app.send(
                LeaveGroupCall(
                    call=chat_call,
                    source=0,
                ),
            )

    async def change_volume(
            self,
            chat_id: int,
            volume: int,
            participant: InputPeer,
    ):
        chat_call = await self._cache.get_full_chat(chat_id)
        if chat_call is not None:
            await self._app.send(
                EditGroupCallParticipant(
                    call=chat_call,
                    participant=participant,
                    muted=False,
                    volume=volume * 100,
                ),
            )

    async def set_call_status(
            self,
            chat_id: int,
            muted_status: Optional[bool],
            paused_status: Optional[bool],
            stopped_status: Optional[bool],
            participant: InputPeer,
    ):
        chat_call = await self._cache.get_full_chat(chat_id)
        if chat_call is not None:
            await self._app.send(
                EditGroupCallParticipant(
                    call=chat_call,
                    participant=participant,
                    muted=muted_status,
                    video_stopped=stopped_status,
                    video_paused=paused_status,
                ),
            )

    async def get_full_chat(self, chat_id: int):
        return await self._cache.get_full_chat(chat_id)

    async def resolve_peer(
            self,
            user_id: Union[int, str],
    ) -> InputPeer:
        return await self._app.resolve_peer(user_id)

    async def get_id(self) -> int:
        return (await self._app.get_me()).id

    def is_connected(self) -> bool:
        return self._app.is_connected

    def no_updates(self):
        return self._app.no_updates

    async def start(self):
        await self._app.start()
