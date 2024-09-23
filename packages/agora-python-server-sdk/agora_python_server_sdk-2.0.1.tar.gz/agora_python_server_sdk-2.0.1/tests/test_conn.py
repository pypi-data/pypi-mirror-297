import pytest
import asyncio
from unittest.mock import patch

class TestRTCConnection:
    @pytest.mark.asyncio
    async def test_connect_with_correct_uid(self):
        # 创建模拟的 RTCConnection 对象
        with patch('your_module.RTCConnection') as mock_rtc_connection:
            # 配置模拟对象的行为
            mock_rtc_connection.return_value.connect.return_value = 0  # 假设连接成功
            mock_rtc_connection.return_value.register_observer.return_value = 0

            # 创建测试用的 Observer
            class TestObserver(IRTCConnectionObserver):
                def __init__(self):
                    self.local_user_id = None

                def on_connected(self, agora_rtc_conn, conn_info, reason):
                    self.local_user_id = conn_info.local_user_id

            test_observer = TestObserver()

            # 创建 RTCConnection 实例并调用 connect
            rtc_conn = mock_rtc_connection()
            rtc_conn.register_observer(test_observer)
            await rtc_conn.connect('token', 'channel_id', 'my_uid')

            # 断言 local_user_id
            assert test_observer.local_user_id == 'my_uid'