import os, time
from dynamixel_sdk import * 

#-------------------|SOMETHING FOR INIT|-----------------------------------------
if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

PROTOCOL_VERSION = 2.0 #--------------|PROTOCOL VERS|----------------------------
LeftMotorID = 1 #------------------------|MOTOR NUM (ID)|------------------------------
RightMotorID = 2
DEVICENAME = '/dev/ttyUSB0'
BAUDRATE = 57600


torqueAddr = 64
presentPositionAddr = 132
goalVelocityAddr = 104
goalPositionAddr = 116

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, 116, 4)
groupSyncRead = GroupSyncRead(portHandler, packetHandler, 132, 4)

def init(startMode):
	# Open port
	if portHandler.openPort():
		print("Succeeded to open the port")
	else:
		print("Failed to open the port")
		print("Press any key to terminate...")
		getch()
		quit()

	# Set port baudrate
	if portHandler.setBaudRate(BAUDRATE):
		print("Succeeded to change the baudrate")
	else:
		print("Failed to change the baudrate")
		print("Press any key to terminate...")
		getch()
		quit()

	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, LeftMotorID, 11, startMode)
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, RightMotorID, 11, startMode)

	if dxl_comm_result != COMM_SUCCESS:
		print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
		print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
		print("Dynamixel has been successfully connected")
		print('Set oper mode success!')
	print('Init complete!')
	print('--------------------------------------------------------------')
	
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 1, 10, 0)
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 2, 10, 1)

#----------|FUNCTION ONLY FOR END 'synceVelocity' FUNCTION (DONT TESTED WITH OTHER FUNCTIONS)|-----------------------
def endCleared(ID1,ID2):
	# Clear syncwrite parameter storage
	groupSyncWrite.clearParam()
	print('Cleared')
	
	#------------------------------------------------------------------------
	
	# Disable Dynamixel#1 Torque
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, torqueAddr, 0)
	
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print("Dynamixel#%d has been successfully disconnected" % ID1)

	# Disable Dynamixel#2 Torque
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID2, torqueAddr, 0)
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print("Dynamixel#%d has been successfully disconnected" % ID2)
	
	# Close port
	portHandler.closePort()
	
def syncVelocity(ID1, ID2, paramSyncSpeed):
	if portHandler.openPort():
		print("Succeeded to open the port")
	else:
		print("Failed to open the port")
		print("Press any key to terminate...")
		getch()
		quit()

	# Set port baudrate
	if portHandler.setBaudRate(BAUDRATE):
		print("Succeeded to change the baudrate")
	else:
		print("Failed to change the baudrate")
		print("Press any key to terminate...")
		getch()
		quit()
	
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, 10, 0)
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID2, 10, 1)
	
	# Enable Dynamixel#1 Torque
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, torqueAddr, 1)
	
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print("Dynamixel#%d has been successfully connected" % ID1)

	# Enable Dynamixel#2 Torque
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID2, torqueAddr, 1)
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print("Dynamixel#%d has been successfully connected" % ID2)
	
	# Add parameter storage for Dynamixel#1 present position value
	dxl_addparam_result = groupSyncRead.addParam(ID1)
	if dxl_addparam_result != True:
	    print("[ID:%03d] groupSyncRead addparam failed" % ID1)
	    quit()
	else: print('Param ID1 successfully added')

	# Add parameter storage for Dynamixel#2 present position value
	dxl_addparam_result = groupSyncRead.addParam(ID2)
	if dxl_addparam_result != True:
	    print("[ID:%03d] groupSyncRead addparam failed" % ID2)
	    quit()
	else: print('Param ID2 successfully added')
	
	# Clear syncwrite parameter storage
	groupSyncRead.clearParam()
	
	#------------------------------------------------------------------------
	
	# Allocate goal position value into byte array
	paramVelocity = [DXL_LOBYTE(DXL_LOWORD(paramSyncSpeed)), DXL_HIBYTE(DXL_LOWORD(paramSyncSpeed)), DXL_LOBYTE(DXL_HIWORD(paramSyncSpeed)), DXL_HIBYTE(DXL_HIWORD(paramSyncSpeed))]

	# Add Dynamixel#1 goal position value to the Syncwrite parameter storage
	dxl_addparam_result = groupSyncWrite.addParam(ID1, paramVelocity)
	if dxl_addparam_result != True:
	 print("[ID:%03d] groupSyncWrite addparam failed" % ID1)
	 quit()

	# Add Dynamixel#2 goal position value to the Syncwrite parameter storage
	dxl_addparam_result = groupSyncWrite.addParam(ID2, paramVelocity)
	if dxl_addparam_result != True:
	 print("[ID:%03d] groupSyncWrite addparam failed" % ID2)
	 quit()

	# Syncwrite goal position
	dxl_comm_result = groupSyncWrite.txPacket()
	if dxl_comm_result != COMM_SUCCESS:
	 print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	
def unsyncVelocity(ID1, ID2, paramSpeed1, paramSpeed2):
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, 10, 0)
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID2, 10, 1)
	
	# Enable Dynamixel#1 Torque
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, torqueAddr, 1)
	
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print("Dynamixel#%d has been successfully connected" % ID1)

	# Enable Dynamixel#2 Torque
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID2, torqueAddr, 1)
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print("Dynamixel#%d has been successfully connected" % ID2)
	
	# Add parameter storage for Dynamixel#1 present position value
	dxl_addparam_result = groupSyncRead.addParam(ID1)
	if dxl_addparam_result != True:
	    print("[ID:%03d] groupSyncRead addparam failed" % ID1)
	    quit()
	else: print('Param ID1 successfully added')

	# Add parameter storage for Dynamixel#2 present position value
	dxl_addparam_result = groupSyncRead.addParam(ID2)
	if dxl_addparam_result != True:
	    print("[ID:%03d] groupSyncRead addparam failed" % ID2)
	    quit()
	else: print('Param ID2 successfully added')
	
	#------------------------------------------------------------------------
	
	while 1:
	    print("Press any key to continue! (or press ESC to quit!)")
	    if getch() == chr(0x1b):
	     break

	    # Allocate goal position value into byte array
	    paramVelocity1 = [DXL_LOBYTE(DXL_LOWORD(paramSpeed1)), DXL_HIBYTE(DXL_LOWORD(paramSpeed1)), DXL_LOBYTE(DXL_HIWORD(paramSpeed1)), DXL_HIBYTE(DXL_HIWORD(paramSpeed1))]
	    paramVelocity2 = [DXL_LOBYTE(DXL_LOWORD(paramSpeed2)), DXL_HIBYTE(DXL_LOWORD(paramSpeed2)), DXL_LOBYTE(DXL_HIWORD(paramSpeed2)), DXL_HIBYTE(DXL_HIWORD(paramSpeed2))]

		
	    # Add Dynamixel#1 goal position value to the Syncwrite parameter storage
	    dxl_addparam_result = groupSyncWrite.addParam(ID1, paramVelocity1)
	    if dxl_addparam_result != True:
	     print("[ID:%03d] groupSyncWrite addparam failed" % ID1)
	     quit()

	    # Add Dynamixel#2 goal position value to the Syncwrite parameter storage
	    dxl_addparam_result = groupSyncWrite.addParam(ID2, paramVelocity2)
	    if dxl_addparam_result != True:
	     print("[ID:%03d] groupSyncWrite addparam failed" % ID2)
	     quit()

	    # Syncwrite goal position
	    dxl_comm_result = groupSyncWrite.txPacket()
	    if dxl_comm_result != COMM_SUCCESS:
	     print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

	    # Clear syncwrite parameter storage
	    groupSyncWrite.clearParam()
	    print('Cleared!')
	
	#------------------------------------------------------------------------
	
	# Disable Dynamixel#1 Torque
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, torqueAddr, 0)
	
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print("Dynamixel#%d has been successfully disconnected" % ID1)

	# Disable Dynamixel#2 Torque
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID2, torqueAddr, 0)
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print("Dynamixel#%d has been successfully disconnected" % ID2)
	
def syncVelocityDegrees(ID1, ID2, paramSyncSpeed, paramSyncDegrees):
	
	if portHandler.openPort():
		print("Succeeded to open the port")
	else:
		print("Failed to open the port")
		print("Press any key to terminate...")
		getch()
		quit()

	# Set port baudrate
	if portHandler.setBaudRate(BAUDRATE):
		print("Succeeded to change the baudrate")
	else:
		print("Failed to change the baudrate")
		print("Press any key to terminate...")
		getch()
		quit()
		
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, 10, 0)
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID2, 10, 1)
	
	# Enable Dynamixel#1 Torque
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, torqueAddr, 1)
	
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print("Dynamixel#%d has been successfully connected" % ID1)

	# Enable Dynamixel#2 Torque
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID2, torqueAddr, 1)
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print("Dynamixel#%d has been successfully connected" % ID2)
	
	# Add parameter storage for Dynamixel#1 present velocity value
	dxl_addparam_result = groupSyncRead.addParam(ID1)
	if dxl_addparam_result != True:
	    print("[ID:%03d] groupSyncRead addparam failed" % ID1)
	    quit()
	else: print('Param ID1 successfully added')

	# Add parameter storage for Dynamixel#2 present velocity value
	dxl_addparam_result = groupSyncRead.addParam(ID2)
	if dxl_addparam_result != True:
	    print("[ID:%03d] groupSyncRead addparam failed" % ID2)
	    quit()
	else: print('Param ID2 successfully added')

	# Clear syncwrite parameter storage
	groupSyncRead.clearParam()
	
	#------------------------------------------------------------------------
	presentPositionNowID1 = 0
	startPositionNow, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, ID1, presentPositionAddr)
	print(startPositionNow)
	
	#--------------------------------------------|VELOCITY PART|--------------------------------------------------------------
	# Allocate goal velocity value into byte array
	paramVelocity = [DXL_LOBYTE(DXL_LOWORD(paramSyncSpeed)), DXL_HIBYTE(DXL_LOWORD(paramSyncSpeed)), DXL_LOBYTE(DXL_HIWORD(paramSyncSpeed)), DXL_HIBYTE(DXL_HIWORD(paramSyncSpeed))]

	# Add Dynamixel#1 goal velocity value to the Syncwrite parameter storage
	dxl_addparam_result = groupSyncWrite.addParam(ID1, paramVelocity)
	if dxl_addparam_result != True:
	 print("[ID:%03d] groupSyncWrite addparam failed" % ID1)
	 quit()

	# Add Dynamixel#2 goal velocity value to the Syncwrite parameter storage
	dxl_addparam_result = groupSyncWrite.addParam(ID2, paramVelocity)
	if dxl_addparam_result != True:
	 print("[ID:%03d] groupSyncWrite addparam failed" % ID2)
	 quit()

	# Syncwrite goal velocity
	dxl_comm_result = groupSyncWrite.txPacket()
	if dxl_comm_result != COMM_SUCCESS:
	 print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

	groupSyncWrite.clearParam()
	#--------------------------------------------|POSITION PART|--------------------------------------------------------------

	print('READING ONLY ID1 BECAUSE ITS SYNCVELOCITY FUNCTION!!!')
	while presentPositionNowID1 <= startPositionNow+paramSyncDegrees:
		presentPositionNowID1, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, ID1, presentPositionAddr)
		presentPositionNowID2, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, ID2, presentPositionAddr)
		print('PositionNow |ID1| = ' + str(presentPositionNowID1) + ' ' + '|ID2| = ' + str(presentPositionNowID2))

	print('Leaving while')
	print('--------------------------------------')
	print('StartPos - ' + str(startPositionNow) + ' | ' + 'NowPos - ' + str(presentPositionNowID1) + ' | ' + 'Razn - ' + str(presentPositionNowID1 - startPositionNow)) 
	#------------------------------------------------------------------------

	
	# Disable Dynamixel#1 Torque
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, torqueAddr, 0)
	
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print("Dynamixel#%d has been successfully disconnected" % ID1)

	# Disable Dynamixel#2 Torque
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID2, torqueAddr, 0)
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print("Dynamixel#%d has been successfully disconnected" % ID2)
	
	# Close port
	portHandler.closePort()
	
def testVelocityDegrees1M(ID1, position, speed):
	if portHandler.openPort():
		print("Succeeded to open the port")
	else:
		print("Failed to open the port")
		print("Press any key to terminate...")
		getch()
		quit()

	if portHandler.setBaudRate(BAUDRATE):
		print("Succeeded to change the baudrate")
	else:
		print("Failed to change the baudrate")
		print("Press any key to terminate...")
		getch()
		quit()
	
	# Enable Dynamixel#1 Torque
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, torqueAddr, 1)
	
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print("Dynamixel#%d has been successfully connected" % ID1)
	    
	#------------------------------------------------------------------------------------------
	dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, ID1, 112, speed) #sets speed
	
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print('Velocity sets!')
	
	#-------------------------------------------------------------------------------------------
	
	posNow, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, ID1, presentPositionAddr)
	print('Position Now: ' + str(posNow))
	
	while 1:
	    # Write goal position
	    presPos, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, ID1, presentPositionAddr)
	    print(presPos)
	    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, ID1, goalPositionAddr, position+4095)
	    if dxl_comm_result != COMM_SUCCESS:
	     print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	    elif dxl_error != 0:
	     print("%s" % packetHandler.getRxPacketError(dxl_error))
	     
	    if not abs(position+4095 - presPos) > 22:
	     dxl_comm_result, dxl_error = packetHandler.clearMultiTurn(portHandler, ID1)
	     if dxl_comm_result != COMM_SUCCESS:
	      print('comm err')
	     elif dxl_error != 0:
	      print('err')
	     else: print('Cleared')
	     
	     break
	
	
	#-------------------------------------------------------------------------------------------
	# Disable Dynamixel#1 Torque
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, torqueAddr, 0)
	
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print("Dynamixel#%d has been successfully disconnected" % ID1)
	    
	posNow, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, ID1, presentPositionAddr)
	print('Position Now: ' + str(posNow))

	# Close port
	portHandler.closePort()

def testSyncVelocityDegrees2M(ID1, ID2, position, speed):
	
	#|OPENING POST|SET BAUDRATE|SET DRIVEMODE|-----------------------------------------------
	if portHandler.openPort():
		print("Succeeded to open the port")
	else:
		print("Failed to open the port")
		print("Press any key to terminate...")
		getch()
		quit()

	if portHandler.setBaudRate(BAUDRATE):
		print("Succeeded to change the baudrate")
	else:
		print("Failed to change the baudrate")
		print("Press any key to terminate...")
		getch()
		quit()
		
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, 10, 0)
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID2, 10, 1)
	#-----------------------------------------------------------------------------------------
	
	#|ENABLING TORUE|-------------------------------------------------------------------------
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, torqueAddr, 1)
	
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print("Dynamixel#%d has been successfully connected" % ID1)
	    
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID2, torqueAddr, 1)
	
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print("Dynamixel#%d has been successfully connected" % ID2)
	#-----------------------------------------------------------------------------------------
	
	#|ADD PARAM SYNC POSITION|----------------------------------------------------------------
	dxl_addparam_result = groupSyncRead.addParam(ID1)
	if dxl_addparam_result != True:
	    print("[ID:%03d] groupSyncRead addparam failed" % ID1)
	    quit()

	dxl_addparam_result = groupSyncRead.addParam(ID2)
	if dxl_addparam_result != True:
	    print("[ID:%03d] groupSyncRead addparam failed" % ID2)
	    quit()
	#-----------------------------------------------------------------------------------------
	
	#|SET VELOCITY|------------------------------------------------------------------------------
	dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, ID1, 112, speed)
	
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print('ID1 Velocity sets!')
	    
	dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, ID2, 112, speed)
	
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print('ID2 Velocity sets!')
	#---------------------------------------------------------------------------------------------
	
	#|ADD SYNC WRITE POSITION PART|-------------------------------------------------------------------
	# Allocate goal position value into byte array
	param_goal_position = [DXL_LOBYTE(DXL_LOWORD(position+4095)), DXL_HIBYTE(DXL_LOWORD(position+4095)), DXL_LOBYTE(DXL_HIWORD(position+4095)), DXL_HIBYTE(DXL_HIWORD(position+4095))]

	# Add Dynamixel#1 goal position value to the Syncwrite parameter storage
	dxl_addparam_result = groupSyncWrite.addParam(ID1, param_goal_position)
	if dxl_addparam_result != True:
	 print("[ID:%03d] groupSyncWrite addparam failed" % ID1)
	 quit()

	# Add Dynamixel#2 goal position value to the Syncwrite parameter storage
	dxl_addparam_result = groupSyncWrite.addParam(ID2, param_goal_position)
	if dxl_addparam_result != True:
	 print("[ID:%03d] groupSyncWrite addparam failed" % ID2)
	 quit()

	# Syncwrite goal position
	dxl_comm_result = groupSyncWrite.txPacket()
	if dxl_comm_result != COMM_SUCCESS:
	 print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

	# Clear syncwrite parameter storage
	groupSyncWrite.clearParam()

	while 1:
	 # Syncread present position
	 dxl_comm_result = groupSyncRead.txRxPacket()
	 if dxl_comm_result != COMM_SUCCESS:
	  print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

	 # Check if groupsyncread data of Dynamixel#1 is available
	 dxl_getdata_result = groupSyncRead.isAvailable(ID1, presentPositionAddr, 4)
	 if dxl_getdata_result != True:
	  print("[ID:%03d] groupSyncRead getdata failed" % ID1)
	  quit()

	 # Check if groupsyncread data of Dynamixel#2 is available
	 dxl_getdata_result = groupSyncRead.isAvailable(ID2, presentPositionAddr, 4)
	 if dxl_getdata_result != True:
	  print("[ID:%03d] groupSyncRead getdata failed" % ID2)
	  quit()

	 # Get Dynamixel#1 present position value
	 dxl1_present_position = groupSyncRead.getData(ID1, presentPositionAddr, 4)

	 # Get Dynamixel#2 present position value
	 dxl2_present_position = groupSyncRead.getData(ID2, presentPositionAddr, 4)

	 #print("[ID:%03d] GoalPos:%03d  PresPos:%03d\t[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL1_ID, dxl_goal_position[index], dxl1_present_position, DXL2_ID, dxl_goal_position[index], dxl2_present_position))

	 if not ((abs(position+4095 - dxl1_present_position) > 20) and (abs(position+4095 - dxl2_present_position) > 20)):
	  dxl_comm_result, dxl_error = packetHandler.clearMultiTurn(portHandler, ID1)
	  if dxl_comm_result != COMM_SUCCESS:
	   print('comm err')
	  elif dxl_error != 0:
	   print('err')
	  else: print('Cleared')
	  posNow, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, ID1, presentPositionAddr)
	  print('Position ID1 Now: ' + str(posNow))
	  
	  dxl_comm_result, dxl_error = packetHandler.clearMultiTurn(portHandler, ID1)
	  if dxl_comm_result != COMM_SUCCESS:
	   print('comm err')
	  elif dxl_error != 0:
	   print('err')
	  else: print('Cleared')
	  posNow, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, ID1, presentPositionAddr)
	  print('Position ID1 Now: ' + str(posNow))
	  
	  dxl_comm_result, dxl_error = packetHandler.clearMultiTurn(portHandler, ID2)
	  if dxl_comm_result != COMM_SUCCESS:
	   print('comm err')
	  elif dxl_error != 0:
	   print('err')
	  else: print('Cleared')
	  posNow, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, ID2, presentPositionAddr)
	  print('Position ID2 Now: ' + str(posNow))
	  
	  break
	
	# Clear syncread parameter storage
	groupSyncRead.clearParam()
	#-----------------------------------------------------------------------------------------------
	
	#|DISABLING TORQUE|-------------------------------------------------------------------------
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, torqueAddr, 0)
	
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print("Dynamixel#%d has been successfully disconnected" % ID1)
	
	dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID2, torqueAddr, 0)
	
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print("Dynamixel#%d has been successfully disconnected" % ID2)
	#---------------------------------------------------------------------------------------------
	
	#|CLOSE PORT|---------------------------------------------------------------------------------
	portHandler.closePort()


# Literally working functions ------------------------------------------------------------------
#-------------------------------------------------------
def openSetPort():
	# Open port --------------------------------------------------------
	if portHandler.openPort():
		print("Succeeded to open the port")
	else:
		print("Failed to open the port")
		print("Press any key to terminate...")
		getch()
		quit()

	# Set port baudrate --------------------------------------------------------
	if portHandler.setBaudRate(BAUDRATE):
		print("Succeeded to change the baudrate")
	else:
		print("Failed to change the baudrate")
		print("Press any key to terminate...")
		getch()
		quit()

def setMotorVelocity(ID1, ID2, speed):
	# Set motor velocity --------------------------------------------------------
	dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, ID1, 112, speed)
	
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print('ID1 Velocity sets!')
	 
	dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, ID2, 112, speed)
	
	if dxl_comm_result != COMM_SUCCESS:
	    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
	elif dxl_error != 0:
	    print("%s" % packetHandler.getRxPacketError(dxl_error))
	else:
	    print('ID2 Velocity sets!')

def cleaningEncoder(ID1, ID2):
	# Cleaning up -------------------------------------------------------- 
	dxl_comm_result, dxl_error = packetHandler.clearMultiTurn(portHandler, ID1)
	if dxl_comm_result != COMM_SUCCESS:
		print('comm err')
	elif dxl_error != 0:
		print('err')
	else: print('Cleared')
	
	clearedPosID1, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, ID1, presentPositionAddr)
	
	dxl_comm_result, dxl_error = packetHandler.clearMultiTurn(portHandler, ID2)
	if dxl_comm_result != COMM_SUCCESS:
		print('comm err')
	elif dxl_error != 0:
		print('err')
	else: print('Cleared')
	
	clearedPosID2, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, ID2, presentPositionAddr)
	
	return clearedPosID1, clearedPosID2

def torque(ID1, ID2, mode):
	if mode:
		dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, torqueAddr, 1)
	
		if dxl_comm_result != COMM_SUCCESS:
			print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
		elif dxl_error != 0:
			print("%s" % packetHandler.getRxPacketError(dxl_error))
		else:
			print("Dynamixel#%d has been successfully connected" % ID1)
			
		dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID2, torqueAddr, 1)
		
		if dxl_comm_result != COMM_SUCCESS:
			print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
		elif dxl_error != 0:
			print("%s" % packetHandler.getRxPacketError(dxl_error))
		else:
			print("Dynamixel#%d has been successfully connected" % ID2)
	else:
		dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, torqueAddr, 0)
	
		if dxl_comm_result != COMM_SUCCESS:
			print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
		elif dxl_error != 0:
			print("%s" % packetHandler.getRxPacketError(dxl_error))
		else:
			print("Dynamixel#%d has been successfully disconnected" % ID1)
			
		dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID2, torqueAddr, 0)
		
		if dxl_comm_result != COMM_SUCCESS:
			print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
		elif dxl_error != 0:
			print("%s" % packetHandler.getRxPacketError(dxl_error))
		else:
			print("Dynamixel#%d has been successfully disconnected" % ID2)
	
def testTurn(ID1, ID2, rotation, position, speed):
	# Opening and set port --------------------------------------------------------
	openSetPort() 
	
	# Set motor direction --------------------------------------------------------
	if rotation == 'R':
		print('Right turn')
		dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, 10, 0)
		dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID2, 10, 0)
	if rotation == 'L':
		print('Left turn')
		dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, 10, 1)
		dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID2, 10, 1)
	
	# Set motor velocity --------------------------------------------------------
	setMotorVelocity(ID1,ID2,speed)
	
	# Cleaning up -------------------------------------------------------- 
	clearedPosID1, clearedPosID2 = cleaningEncoder(ID1,ID2)
	print('clearedPosition ID1: ' + str(clearedPosID1))
	print('clearedPosition ID2: ' + str(clearedPosID2))
	
	# Enabling torque -------------------------------------------------------- 
	torque(ID1,ID2,1)
	
	# Add sync param -------------------------------------------------------- 
	dxl_addparam_result = groupSyncRead.addParam(ID1)
	if dxl_addparam_result != True:
	    print("[ID:%03d] groupSyncRead addparam failed" % ID1)
	    quit()

	dxl_addparam_result = groupSyncRead.addParam(ID2)
	if dxl_addparam_result != True:
	    print("[ID:%03d] groupSyncRead addparam failed" % ID2)
	    quit()
	
	# Add sync write part -------------------------------------------------------- 
	
	# Allocate goal position value into byte array
	paramPositionID1 = [DXL_LOBYTE(DXL_LOWORD(position+clearedPosID1)), DXL_HIBYTE(DXL_LOWORD(position+clearedPosID1)), DXL_LOBYTE(DXL_HIWORD(position+clearedPosID1)), DXL_HIBYTE(DXL_HIWORD(position+clearedPosID1))]
	paramPositionID2 = [DXL_LOBYTE(DXL_LOWORD(position+clearedPosID2)), DXL_HIBYTE(DXL_LOWORD(position+clearedPosID2)), DXL_LOBYTE(DXL_HIWORD(position+clearedPosID2)), DXL_HIBYTE(DXL_HIWORD(position+clearedPosID2))]

	# Add Dynamixel#1 goal position value to the Syncwrite parameter storage
	dxl_addparam_result = groupSyncWrite.addParam(ID1, paramPositionID1)
	if dxl_addparam_result != True:
	 print("[ID:%03d] groupSyncWrite addparam failed" % ID1)
	 quit()

	# Add Dynamixel#2 goal position value to the Syncwrite parameter storage
	dxl_addparam_result = groupSyncWrite.addParam(ID2, paramPositionID2)
	if dxl_addparam_result != True:
	 print("[ID:%03d] groupSyncWrite addparam failed" % ID2)
	 quit()

	# Syncwrite goal position
	dxl_comm_result = groupSyncWrite.txPacket()
	if dxl_comm_result != COMM_SUCCESS:
	 print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

	# Clear syncwrite parameter storage
	groupSyncWrite.clearParam()
	
	# Add sync read part --------------------------------------------------------
	while 1:
	 # Syncread present position
	 dxl_comm_result = groupSyncRead.txRxPacket()
	 if dxl_comm_result != COMM_SUCCESS:
	  print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

	 # Check if groupsyncread data of Dynamixel#1 is available
	 dxl_getdata_result = groupSyncRead.isAvailable(ID1, presentPositionAddr, 4)
	 if dxl_getdata_result != True:
	  print("[ID:%03d] groupSyncRead getdata failed" % ID1)
	  quit()

	 # Check if groupsyncread data of Dynamixel#2 is available
	 dxl_getdata_result = groupSyncRead.isAvailable(ID2, presentPositionAddr, 4)
	 if dxl_getdata_result != True:
	  print("[ID:%03d] groupSyncRead getdata failed" % ID2)
	  quit()

	 # Get Dynamixel#1 present position value
	 presentPositionID1 = groupSyncRead.getData(ID1, presentPositionAddr, 4)

	 # Get Dynamixel#2 present position value
	 presentPositionID2 = groupSyncRead.getData(ID2, presentPositionAddr, 4)

	 #print("[ID:%03d] GoalPos:%03d  PresPos:%03d\t[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL1_ID, dxl_goal_position[index], dxl1_present_position, DXL2_ID, dxl_goal_position[index], dxl2_present_position))

	 if not ((abs(position+clearedPosID1 - presentPositionID1) > 20) and (abs(position+clearedPosID2 - presentPositionID2) > 20)):
	  cleaningEncoder(ID1,ID2)
	  break
	
	# Clear syncread parameter storage
	groupSyncRead.clearParam()
	
	# Disabling torque --------------------------------------------------------
	torque(ID1,ID2,0)
	
	# Close port --------------------------------------------------------
	portHandler.closePort()
	
def testDirect(ID1, ID2, rotation, position, speed):
	# Opening and set port --------------------------------------------------------
	openSetPort() 
	
	# Set motor direction --------------------------------------------------------
	if rotation == 'F':
		print('Forward')
		dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, 10, 0)
		dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID2, 10, 1)
	if rotation == 'B':
		print('Backward')
		dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID1, 10, 1)
		dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID2, 10, 0)
	
	# Set motor velocity --------------------------------------------------------
	setMotorVelocity(ID1,ID2,speed)
	
	# Cleaning up -------------------------------------------------------- 
	clearedPosID1, clearedPosID2 = cleaningEncoder(ID1,ID2)
	print('clearedPosition ID1: ' + str(clearedPosID1))
	print('clearedPosition ID2: ' + str(clearedPosID2))
	
	# Enabling torque -------------------------------------------------------- 
	torque(ID1,ID2,1)
	
	# Add sync param -------------------------------------------------------- 
	dxl_addparam_result = groupSyncRead.addParam(ID1)
	if dxl_addparam_result != True:
	    print("[ID:%03d] groupSyncRead addparam failed" % ID1)
	    quit()

	dxl_addparam_result = groupSyncRead.addParam(ID2)
	if dxl_addparam_result != True:
	    print("[ID:%03d] groupSyncRead addparam failed" % ID2)
	    quit()
	
	# Add sync write part -------------------------------------------------------- 
	
	# Allocate goal position value into byte array
	paramPositionID1 = [DXL_LOBYTE(DXL_LOWORD(position+clearedPosID1)), DXL_HIBYTE(DXL_LOWORD(position+clearedPosID1)), DXL_LOBYTE(DXL_HIWORD(position+clearedPosID1)), DXL_HIBYTE(DXL_HIWORD(position+clearedPosID1))]
	paramPositionID2 = [DXL_LOBYTE(DXL_LOWORD(position+clearedPosID2)), DXL_HIBYTE(DXL_LOWORD(position+clearedPosID2)), DXL_LOBYTE(DXL_HIWORD(position+clearedPosID2)), DXL_HIBYTE(DXL_HIWORD(position+clearedPosID2))]

	# Add Dynamixel#1 goal position value to the Syncwrite parameter storage
	dxl_addparam_result = groupSyncWrite.addParam(ID1, paramPositionID1)
	if dxl_addparam_result != True:
	 print("[ID:%03d] groupSyncWrite addparam failed" % ID1)
	 quit()

	# Add Dynamixel#2 goal position value to the Syncwrite parameter storage
	dxl_addparam_result = groupSyncWrite.addParam(ID2, paramPositionID2)
	if dxl_addparam_result != True:
	 print("[ID:%03d] groupSyncWrite addparam failed" % ID2)
	 quit()

	# Syncwrite goal position
	dxl_comm_result = groupSyncWrite.txPacket()
	if dxl_comm_result != COMM_SUCCESS:
	 print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

	# Clear syncwrite parameter storage
	groupSyncWrite.clearParam()
	
	# Add sync read part --------------------------------------------------------
	while 1:
	 # Syncread present position
	 dxl_comm_result = groupSyncRead.txRxPacket()
	 if dxl_comm_result != COMM_SUCCESS:
	  print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

	 # Check if groupsyncread data of Dynamixel#1 is available
	 dxl_getdata_result = groupSyncRead.isAvailable(ID1, presentPositionAddr, 4)
	 if dxl_getdata_result != True:
	  print("[ID:%03d] groupSyncRead getdata failed" % ID1)
	  quit()

	 # Check if groupsyncread data of Dynamixel#2 is available
	 dxl_getdata_result = groupSyncRead.isAvailable(ID2, presentPositionAddr, 4)
	 if dxl_getdata_result != True:
	  print("[ID:%03d] groupSyncRead getdata failed" % ID2)
	  quit()

	 # Get Dynamixel#1 present position value
	 presentPositionID1 = groupSyncRead.getData(ID1, presentPositionAddr, 4)

	 # Get Dynamixel#2 present position value
	 presentPositionID2 = groupSyncRead.getData(ID2, presentPositionAddr, 4)

	 #print("[ID:%03d] GoalPos:%03d  PresPos:%03d\t[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL1_ID, dxl_goal_position[index], dxl1_present_position, DXL2_ID, dxl_goal_position[index], dxl2_present_position))

	 if not ((abs(position+clearedPosID1 - presentPositionID1) > 20) and (abs(position+clearedPosID2 - presentPositionID2) > 20)):
	  cleaningEncoder(ID1,ID2)
	  break
	
	# Clear syncread parameter storage
	groupSyncRead.clearParam()
	
	# Disabling torque --------------------------------------------------------
	torque(ID1,ID2,0)
	
	# Close port --------------------------------------------------------
	portHandler.closePort()
	
def square():
	for i in range(4):
		testDirect(1,2,'F',4000,200)
		testTurn(1,2,'R',2320,200)

def checkPosition(ID1, ID2):
	
	cleaningEncoder(ID1,ID2)
	
	startPosID1, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, ID1, presentPositionAddr)
	startPosID2, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, ID2, presentPositionAddr)
	print('Start pos ID1: ' + str(startPosID1))
	print('Start pos ID2: ' + str(startPosID2))

	while 1:
		posNowID1, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, ID1, presentPositionAddr)
		posNowID2, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, ID2, presentPositionAddr)
		
		print("Press any key to continue! (or press ESC to quit!)")
		if getch() == chr(0x1b):
			print('Diff ID1: ' + str(posNowID1-startPosID1) + ' ID2: ' + str(posNowID2-startPosID2))
			cleaningEncoder(ID1,ID2)
			break
		
		print('Pos now ID1: ' + str(posNowID1) + ' ID2: ' + str(posNowID2))
			
