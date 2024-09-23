import asyncio  
import pytest  

import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sdk_dir = os.path.dirname(script_dir)
# sdk_dir = os.path.dirname(os.path.dirname(script_dir))
if sdk_dir not in sys.path:
    sys.path.insert(0, sdk_dir)

import time
import os
import sys
import datetime
import threading

from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, AudioSubscriptionOptions, RTCConnConfig
from agora.rtc.rtc_connection_observer import IRTCConnectionObserver
from agora.rtc.rtc_connection import RTCConnection
from agora.rtc.agora_base import *


class MockObserver(IRTCConnectionObserver):
    def __init__(self):
        self.connected_info = None
        self.event = asyncio.Event() 

    def on_connected(self, agora_rtc_conn, conn_info, reason):
        print("Observer: on_connected called")
        self.connected_info = conn_info
        self.event.set()  # 触发事件，表示已连接
        print(f"Observer: Connected with local_user_id: {conn_info.local_user_id}")
        print("Observer: thread id", threading.get_ident())

# 测试用例
@pytest.mark.asyncio
async def test_on_connected_called_with_correct_user_id():
    print("Test: Starting test_on_connected_called_with_correct_user_id")
    # 创建一个RTCConnection实例
    #---------------1. Init SDK
    config = AgoraServiceConfig()
    config.appid = "aab8b8f5a8cd4469a63042fcfafe7063"
    config.log_path = "/Users/dingyusong/Downloads/tests_log/agorasdk.log"

    agora_service = AgoraService()
    agora_service.initialize(config)

    #---------------2. Create Connection
    con_config = RTCConnConfig(
        client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
        channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
    )

    connection = agora_service.create_rtc_connection(con_config)
    
    # 创建一个具体的观察者实例
    observer = MockObserver()
    
    # 注册观察者
    connection.register_observer(observer)
    
    print("before connect")
    # 调用connect方法  
    sample_token = "aab8b8f5a8cd4469a63042fcfafe7063"  
    channel_id = "dummy_channel"  
    uid = "1"  
    connection.connect(sample_token, channel_id, uid)  
    print("connect: thread id", threading.get_ident())
    print("after connect")

    # 等待 on_connected 被调用
    # observer.event.wait()  # 等待最多5秒
    await observer.event.wait()  # 等待事件被设置
    print("after connect2222")

    # try:
    #     await asyncio.wait_for(observer.event.wait(), timeout=5)
    # except asyncio.TimeoutError:
    #     assert False, "on_connected was not called within the timeout period"

    print("after connect3333")
    # 验证 local_user_id 是否与 uid 一致
    assert observer.connected_info is not None, "on_connected should have been called"
    assert observer.connected_info.local_user_id == uid, "local_user_id should match the provided uid"

# 运行测试
# if __name__ == "__main__":
#     pytest.main()
