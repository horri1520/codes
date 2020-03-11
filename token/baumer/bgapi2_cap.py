#OpenCV,numpy,Harvesterをロード
import cv2
import time
import os
import datetime
import numpy as np 
from harvesters.core import Harvester

#Harvesterオブジェクト作成
h = Harvester()

#ctiファイル(GeniCamシステムファイル)をロード
#USB3用
#h.add_cti_file("bgapi2_usb.cti")
#GigE用
h.add_cti_file("./libbgapi2_gige.cti")

#デバイスリストを更新
h.update_device_info_list()

#デバイスリストのインデックスは0から始まる
print(h.device_info_list)
#インデックス0のデバイスオブジェクトを作成
ia = h.create_image_acquirer(0)
print("open first device")	

#デバイスの設定変更はdevice.node_map.のあとにNode名を指定し.valueを取得したり操作する
#Node名はSDK付属ビュアーのCameraExplorerで右上のProfileをGeniCamGuruに変更することで確認可能(パラメータ名に半角スペースは不要)
#利用可能なNode一覧表示
#print(dir(ia.device.node_map))
#print(dir(ia._data_streams[0].local_node_map))

#露光時間を32000μsに変更
ia.device.node_map.ExposureTime.value = 32000
print("Exposure = %dus" %ia.device.node_map.ExposureTime.value)

#フレームレートを9fpsに変更
ia.device.node_map.AcquisitionFrameRateEnable.value = True
ia.device.node_map.AcquisitionFrameRate.value = 9
print("FrameRate = %dfps" %ia.device.node_map.AcquisitionFrameRate.value)
#パケットサイズ表示
#ia.device.node_map.DeviceStreamChannelPacketSize.value = 9
print("PacketSize = %dbyte" %ia.device.node_map.DeviceStreamChannelPacketSize.value)

#HDR設定
ia.device.node_map.HDREnable.value = "On"
ia.device.node_map.AcquisitionFrameRate.value = 5
ia.device.node_map.HDRExposureRatio.value = 160
ia.device.node_map.HDRPotentialAbs.value = 21
ia.device.node_map.HDRIndex.value = 0

#横画素数と縦画素数を取得
_width = ia.device.node_map.Width.value
_height = ia.device.node_map.Height.value
print("Width = %d / Height = %d" %(_width, _height) )

#PixelFormatを取得
#画像サイズが変わる設定はimage_acquisitionがStopの状態の時のみ有効
#ia.device.node_map.PixelFormat.value = "BGR8"
_pixelformat = ia.device.node_map.PixelFormat.value
print("PixelFormat = %s"  %_pixelformat)

#TriggerModeを変更
ia.device.node_map.TriggerMode.value = "Off"
#ia.device.node_map.TriggerMode.value = "On"
_triggermode = ia.device.node_map.TriggerMode.value
print("TriggerMode = %s"  %ia.device.node_map.TriggerMode.value)

#検知するTriggerソースをSoftwareに固定（デフォルトは全てのソースとなる"All"）
#ia.device.node_map.TriggerSource.value = "Software"

#StreamをStartしてデータ出力開始
ia.start_image_acquisition()

#カラー出力ならホワイトバランス調整
if "Mono" not in _pixelformat :
	ia.device.node_map.BalanceWhiteAuto.value = "Once"
	print("White balance was adjusted!")

_key = 0
cv2.namedWindow("Preview: Press ESC key for exit / Precc C Key SoftTrigger", cv2.WINDOW_AUTOSIZE)
#ライブ表示
#ESCキーを押すと停止
while _key != 27 :
	_key = cv2.waitKey(16)
	#トリガーモード時
	if 	_triggermode == "On" :
		#Cキーを押すとソフトトリガ送信
		while _key != 99 :
			_key = cv2.waitKey(16)
			if _key == 27 :
				break

		#SoftwareTriggger発行
		ia.device.node_map.TriggerSoftware.execute()

	#新しいデータが来たらbufferに格納
	with ia.fetch_buffer() as buffer :
		#バッファ情報にアクセス
		component = buffer.payload.components[0]

		#バッファ内のnumpy配列にアクセス		
		_rawimg = component.data
		#格納されている配列は1Dなのでreshapeで2Dに変換
		if _pixelformat == 'BGR8' or _pixelformat == 'RGB8' :
			_2Dimg = component.data.reshape(component.height,component.width,3)
		else :
			_2Dimg = component.data.reshape(component.height,component.width)

		#OpenCVの表示APIでバッファ内のデータ表示
		if 'Bayer' in _pixelformat :
			#Bayerならカラーデータに変換
			_2Dcolorimg = cv2.cvtColor(_2Dimg,cv2.COLOR_BAYER_GB2RGB)

			#8bit以外なら表示用データ作成
			if '8' not in _pixelformat :
				_display = cv2.convertScaleAbs(_2Dcolorimg, alpha = 0.0625)
			else :
				_display = _2Dcolorimg
		elif _pixelformat == 'BGR8' or _pixelformat == 'RGB8' :
			_display = _2Dimg
		else :
			#8bit以外なら表示用データ作成
			if '8' not in _pixelformat :
				_display = cv2.convertScaleAbs(_2Dimg, alpha = 0.0625)
			else :
				_display = _2Dimg

		#リサイズ
		dt_now = datetime.datetime.now()
		dt_str = dt_now.strftime('%Y-%m-%d_%H-%M-%S-%f')
		f_name = dt_str + ".jpg"
		save_f_path = os.path.join("./data", f_name)
		if _height > 1080 :
			_resize = cv2.resize(_display, dsize=None, fx=0.33, fy=0.33)
			cv2.imshow("Preview: Press ESC key for exit / Precc C Key SoftTrigger" , _resize)
			cv2.imwrite(save_f_path, _resize)
		else :
			cv2.imshow("Preview: Press ESC key for exit / Precc C Key SoftTrigger" , _display)
			cv2.imwrite(save_f_path, _display)
		#[0,0]の輝度値表示
		#print('RAW_data[0,0]-recieved[{0}]: {1}'.format(ia.statistics.num_images, _2Dimg[0][0]))
		#print('BGR_data[0,0]-recieved[{0}]: {1}'.format(ia.statistics.num_images, _2Dcolorimg[0][0]))
		#print('8bitConvert_data[0,0]-recieved[{0}]: {1}'.format(ia.statistics.num_images, _display[0][0]))

		#StreamのNode参照：転送ステータスチェック
		print("PacketReceiveComplete = %d" %ia._data_streams[0].local_node_map.PacketReceiveComplete.value)
		print("PacketReceiveIncomplete = %d" %ia._data_streams[0].local_node_map.PacketReceiveIncomplete.value)
		print("PacketResendRequestSingle = %d" %ia._data_streams[0].local_node_map.PacketResendRequestSingle.value)
	pass

#StreamをStopしてデータ出力停止
ia.stop_image_acquisition()
#デバイスオブジェクトを破棄
ia.destroy()
#Harvesterオブジェクトを解放
h.reset()
#cv2プレビュー画面破棄
cv2.destroyAllWindows()

quit()

