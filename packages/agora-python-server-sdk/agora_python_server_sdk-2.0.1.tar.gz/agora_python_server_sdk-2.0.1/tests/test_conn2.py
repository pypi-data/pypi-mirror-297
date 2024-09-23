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
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, AudioSubscriptionOptions, RTCConnConfig
from agora.rtc.rtc_connection_observer import IRTCConnectionObserver
from agora.rtc.rtc_connection import RTCConnection
from agora.rtc.agora_base import *

class MockObserver(IRTCConnectionObserver):  
    def __init__(self):  
        self.event = asyncio.Event()  
        self.conn_info = None  
  
    def on_connected(self, rtc_conn, conn_info, reason):  
        print("on_connected")
        self.conn_info = conn_info  
        self.event.set()  # 设置事件，表示回调已被调用  

# 使用 pytest-asyncio 的异步测试  
@pytest.mark.asyncio  
async def test_connection_connect_with_observer():  
        # 创建RTCConnection实例  
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
  
        # 创建MockObserver实例  
        observer = MockObserver()  
  
        # 注册观察者  
        connection.register_observer(observer)  
        print("before connect")
        # 调用connect方法  
        sample_token = "aab8b8f5a8cd4469a63042fcfafe7063"  
        channel_id = "dummy_channel"  
        uid = "1"  
        connection.connect(sample_token, channel_id, uid)  
        
        print("after connect")
        # 等待事件被设置，表示 on_connected 已被调用  
        await observer.event.wait()  

        # 验证 conn_info 是否被正确设置  
        assert observer.conn_info is not None  
        assert observer.conn_info.local_user_id == "dummy_uid"  
  
# if __name__ == '__main__':  
#     test_connection_connect_with_observer()