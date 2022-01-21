###################################################################################################
# Hệ điều hành - Đồ án nhóm 1
# NTFS
# Người thực hiện: Bùi Quang Bảo - 19120454

# Tổng quan kết quả thực hiện, quá trình cài đặt: Đã được nêu rõ trong báo cáo

# Cách sử dụng: python read-ntfs.py {Ký tự ổ đĩa cần đọc} {Số bytes muốn đọc ở MFT}

# Ví dụ:
# python read-ntfs.py F 1024
# Đọc ổ đĩa F (USB - định dạng NTFS), đọc BPB, tìm vị trí sector đầu tiên của MFT và đọc 1024 bytes
###################################################################################################

# sys được sử dụng để đọc tham số dòng lệnh
import sys
# numpy được sử dụng để reshape dữ liệu dạng list, 
# thuận tiện trong quá trình in ra màn hình
import numpy as np
# math được dùng để thực hiện 1 số thao tác toán
import math


# Hàm chuyển đổi HEX -> DEC
def hex_to_dec(hex_str):
    return int(hex_str, 16)

# Hàm chuyển đổi HEX -> ASCII
def hex_to_ascii(hex_str):
    return bytearray.fromhex(hex_str).decode()

# Đọc BPB (Bios Parameter Block)
class BPB:
    def __init__(self, diskname, num_of_rows_to_read):
        self.read_successfully = False
        self.data_list = []
        with open(diskname,'rb') as f:
            self.read_successfully = True
            # ========== Đọc dữ liệu ổ đĩa (binary) và lưu vào 'data_list' ==========
            data = f.read(num_of_rows_to_read * 16)
            self.data_list = np.array(["{:02X}".format(char) for char in data])
            self.data_list = np.reshape(self.data_list, (-1,16))
            # =============== Đọc các thông tin quan trọng của ổ đĩa ================
            # Số bytes/sector
            # 0B - 2 bytes
            self.bytes_per_sector = hex_to_dec(self.data_list[0][12] + self.data_list[0][11])
            # Số sectors/cluster
            # 0D - 1 byte
            self.sectors_per_cluster = hex_to_dec(self.data_list[0][13])
            # Số sectors/track
            # 18 - 2 bytes
            self.sectors_per_track = hex_to_dec(self.data_list[1][9] + self.data_list[1][8])
            # Số mặt đĩa
            # 1A - 2 bytes
            self.number_of_heads = hex_to_dec(self.data_list[1][11] + self.data_list[1][10])
            # Cluster bắt đầu
            # 30 - 8 bytes
            temp = [self.data_list[3][7-i] for i in range(8)]
            self.logical_cluster_number_for_MFT = hex_to_dec(''.join(temp))
            # Sector bắt đầu
            # Sector = X * Sc
            self.physical_sector_number_for_MFT = self.logical_cluster_number_for_MFT * self.sectors_per_cluster
    
    # In dữ liệu đọc được từ BPB và 1 số thông tin quan trọng ra màn hình console
    def print_BPB(self):
        if self.read_successfully:
            print('BPB - Bios Parameter Block:')
            # In ra màn hình data_list
            print('       0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F')
            print('       |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |')
            for i, row in enumerate(self.data_list):
                print('{:02}'.format(i), end=' -- ')
                for item in row:
                    print(f'{item} ', end='')
                print('    ', end='')
                for item in row:
                    try:
                        if item == '00':
                            print(' ', end='_')
                        elif not item in ['0A','0B','0C','0D']:
                            print(hex_to_ascii(item), end='_')
                        else:
                            print('\\n', end='_')
                    except:
                        print('.', end='_')
                print('')
            print('')
            # In thông tin ra màn hình
            print('=================================================')
            print('THÔNG TIN Ổ ĐĨA:')
            print(f'Kích thước 1 sector: {self.bytes_per_sector} (bytes/sector)')
            print(f'Số sectors/cluster: Sc = {self.sectors_per_cluster}')
            print(f'Số sectors/track: {self.sectors_per_track}')
            print(f'Số mặt đĩa: {self.number_of_heads}')
            print(f'Cluster bắt đầu của MFT: {self.logical_cluster_number_for_MFT}')
            print(f'Sector bắt đầu của MFT: {self.physical_sector_number_for_MFT} (= {self.logical_cluster_number_for_MFT} x {self.sectors_per_cluster})')
            print('=================================================\n\n')
        else:
            print('>> Quá trình đọc dữ liệu từ đĩa bị lỗi.')

# Đọc dữ liệu sector
class Sector:
    def __init__(self, diskname, num_of_rows_to_read, sector_size, sector_number):
        self.read_successfully = False
        self.data_list = []
        self.sector_number = sector_number
        with open(diskname,'rb') as f:
            self.read_successfully = True
            # ======================== Nhảy tới sector cần đọc ==========================
            for i in range(sector_number):
                data = f.read(sector_size)
                # if i % 100000 == 0:
                #     print(f'>> {i}')
            # ================== Đọc dữ liệu (binary) vào 'data_list' ===================
            data = f.read(num_of_rows_to_read * 16)
            self.data_list = np.array(["{:02X}".format(char) for char in data])
            self.data_list = np.reshape(self.data_list, (-1,16))
    
    # In dữ liệu đọc được của sector ra màn hình console
    def print_sector(self):
        if self.read_successfully:
            print(f'Sector {self.sector_number}:')
            # In ra màn hình data_list
            print('       0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F')
            print('       |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |')
            for i, row in enumerate(self.data_list):
                print('{:02}'.format(i), end=' -- ')
                for item in row:
                    print(f'{item} ', end='')
                print('    ', end='')
                for item in row:
                    try:
                        if item == '00':
                            print(' ', end='_')
                        elif not item in ['0A','0B','0C','0D']:
                            print(hex_to_ascii(item), end='_')
                        else:
                            print('\\n', end='_')
                    except:
                        print('.', end='_')
                print('')
            print('')
        else:
            print('>> Quá trình đọc dữ liệu từ đĩa bị lỗi.')



# Tiến hành xử lý tham số và thực hiện đọc ổ đĩa
if len(sys.argv) <= 2:
    print('\n>> Cách sử dụng: python read-ntfs.py {Ký tự ổ đĩa} {Số lượng bytes cần đọc ở sector}')
    print('>> Ví dụ: python read-ntfs.py F 1024\n')
else:
    try:
        print('\n-----------------------------------------------------------')
        # Xử lý tham số dòng lệnh
        diskname = f"\\\\.\\{sys.argv[1]}:"
        num_of_bytes_to_read = int(sys.argv[2])
        num_of_rows_to_read = int(math.ceil(num_of_bytes_to_read / 16))
        # Thông tin
        print(f'Ổ đĩa: {diskname}')
        print(f'Đọc {num_of_bytes_to_read} bytes ~ {num_of_rows_to_read} dòng (16 bytes/dòng)\n')
        # ---------- Xử lý ----------
        # Đọc BPB
        bpb = BPB(diskname, 64)
        bpb.print_BPB()
        # Đọc sector
        # sector = Sector(diskname, num_of_rows_to_read, bpb.bytes_per_sector, 0) # Just to test
        sector = Sector(diskname, num_of_rows_to_read, bpb.bytes_per_sector, bpb.physical_sector_number_for_MFT)
        sector.print_sector()
        print('-------------------------------------------------------------\n')
    except:
        print('>\n> Xảy ra lỗi, xin mời nhập đúng định dạng tham số\n>')
        print(sys.argv)