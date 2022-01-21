// exception.cc 
//	Entry point into the Nachos kernel from user programs.
//	There are two kinds of things that can cause control to
//	transfer back to here from user code:
//
//	syscall -- The user code explicitly requests to call a procedure
//	in the Nachos kernel.  Right now, the only function we support is
//	"Halt".
//
//	exceptions -- The user code does something that the CPU can't handle.
//	For instance, accessing memory that doesn't exist, arithmetic errors,
//	etc.  
//
//	Interrupts (which can also cause control to transfer from user
//	code into the Nachos kernel) are handled elsewhere.
//
// For now, this only handles the Halt() system call.
// Everything else core dumps.
//
// Copyright (c) 1992-1993 The Regents of the University of California.
// All rights reserved.  See copyright.h for copyright notice and limitation 
// of liability and disclaimer of warranty provisions.

#include "copyright.h"
#include "system.h"
#include "syscall.h"

//----------------------------------------------------------------------
// ExceptionHandler
// 	Entry point into the Nachos kernel.  Called when a user program
//	is executing, and either does a syscall, or generates an addressing
//	or arithmetic exception.
//
// 	For system calls, the following is the calling convention:
//
// 	system call code -- r2
//		arg1 -- r4
//		arg2 -- r5
//		arg3 -- r6
//		arg4 -- r7
//
//	The result of the system call, if any, must be put back into r2. 
//
// And don't forget to increment the pc before returning. (Or else you'll
// loop making the same system call forever!
//
//	"which" is the kind of exception.  The list of possible exceptions 
//	are in machine.h.
//----------------------------------------------------------------------

#define MaxFileLength 32
// Ham tang program counter
void IncProgCounter(){
    int counter=machine->ReadRegister(PCReg);
    machine->WriteRegister(PrevPCReg,counter);
    counter=machine->ReadRegister(NextPCReg);
    machine->WriteRegister(PCReg,counter);
    machine->WriteRegister(NextPCReg,counter+4);
}
/*
Input: - User space address (int)
       - Limit of buffer (int)
Output:- Buffer (char*)
Purpose: Copy buffer from User memory space to System memory space
*/
char* User2System(int virtAddr, int limit)
{
	int i;
	int oneChar;
	char* kernelBuf = NULL;
	kernelBuf = new char[limit + 1];
	if (kernelBuf == NULL)
		return kernelBuf;
		
	memset(kernelBuf, 0, limit + 1);
	
	for (i = 0; i < limit; i++)
	{
		machine->ReadMem(virtAddr + i, 1, &oneChar);
		kernelBuf[i] = (char)oneChar;
		if (oneChar == 0)
			break;
	}
	return kernelBuf;
}
/*
Input: - User space address (int)
       - Limit of buffer (int)
       - Buffer (char[])
Output:- Number of bytes copied (int)
Purpose: Copy buffer from System memory space to User  memory space
*/
int System2User(int virtAddr, int len, char* buffer)
{
	if (len < 0) return -1;
	if (len == 0)return len;
	int i = 0;
	int oneChar = 0;
	do{
		oneChar = (int)buffer[i];
		machine->WriteMem(virtAddr + i, 1, oneChar);
		i++;
	} while (i < len && oneChar != 0);
	return i;
}

void EH_ReadInt(){
    double re=0;
    int maxSize=20;
    char *value=new char[maxSize];
    int bytes=gSynchConsole->Read(value,maxSize);//Doc vao chuoi duoc nhap tu console va do dai chuoi
    int i=0,n=1;
    int countDot=0;
    bool isNegative=false;
    // Kiem tra so am hay duong
    if(value[i]=='-'){
        i++;
        isNegative=true;
    }
    // Duyet qua chuoi ki tu doc duoc
    for(i;i<bytes;i++){
        // Neu trong chuoi chi ton tai cac chu so va toi da 1 dau cham(neu la so thuc)
        // thi van hop le, nguoc lai tra ve 0
        if(value[i]>'9' || value[i]<'0')
            if(value[i]!='.' || (value[i]=='.' && countDot==1)){
                machine->WriteRegister(2,0); //tra ve 0 neu chuoi co chua ki tu khac chu so hoac co nhieu hon 1 dau cham
                delete []value;
                return;
            }
            else
                countDot++;
        else //dem so luong dau cham, dong thoi tinh gia tri chuoi 
            if(countDot==0)
                re=re*10+(value[i]-'0');
            else{
                n*=10;
                re+=(value[i]-'0')/n;
            }
    }
    //Neu la so am thi doi dau
    if(isNegative) re=-re;
    machine->WriteRegister(2,(int)re);//tra ve ket qua
    delete []value;
}

void EH_PrintInt(){
    int value=machine->ReadRegister(4); //doc vao gia tri so nguyen tu thanh ghi
    char* re;
    int reverse=0;
    int numberOfDigit=0;
    int reLength=0;
    bool isNegative=false;
    int i=0;
    // Neu la 0 thi tra ve chuoi "0\0"
    if(value==0){
        gSynchConsole->Write("0\0",2);
        return;
    }
    // Kiem tra xem co phai so am hay khong, neu co thi doi dau,
    if(value<0){
        isNegative=true;
        value=-value;
        reLength++;
    }
    // tim so dao nguoc cua so da biet
    while(value>0){
        reverse=reverse*10 + value%10;
        value/=10;
        numberOfDigit++;
    }
    reLength+=numberOfDigit;
    re=new char[reLength+1];
    // neu so ban dau la am thi them dau '-' vao dau chuoi
    if(isNegative) {
        re[0]='-';
    }
    // chuyen so dao nguoc thanh chuoi ki tu
    for(i=reLength-numberOfDigit;i<reLength;i++){
        re[i]=reverse%10+'0';
        reverse/=10;
    }
    re[reLength]='\0';// them null vao cuoi chuoi tra ve
    gSynchConsole->Write(re, reLength+1);//ghi ket qua len man hinh
    delete[] re;
}

void EH_ReadChar(){
    int maxSize = 10;
    char* value = new char[maxSize];
    int byte = gSynchConsole->Read(value,maxSize);
	
    //Boi vi kich thuoc char = 1 byte --> Ta xet cac truong hop:
    // 1. Nhap dung 1 ky tu
    // 2. Khong nhap ki tu nao (ky tu rong)    
    // 3. Nhap nhieu hon 1 ky tu (vi du: 2,3,4,5... ky tu)
    switch(byte){
    	case 1:{
		char character = value[0];
		machine->WriteRegister(2,character);
		break;			
	}
	case 0:{
		printf("Ban chua nhap ki tu ! \n");
		machine->WriteRegister(2,0);
		break;
	}
	default:{
		printf("Ban da nhap nhieu hon 1 ky tu !!!! Vui long thu lai \n");
		machine->WriteRegister(2,0);
		break;	
	}
    }
    delete[] value;
}

void EH_PrintChar(){
    //Doc tu thanh ghi
    char character = (char)machine->ReadRegister(4);
    //Xuat 1 ky tu (tuong ung 1 byte) ra man hinh
    gSynchConsole->Write(&character, 1);
}

void EH_ReadString()
{
	int virtAddr,len;
	char* buffer;
	int size=0;
	int i=0;
	virtAddr=machine->ReadRegister(4);//Doc vi tri cua chuoi
	len=machine->ReadRegister(5);//Doc do dai cua chuoi
	buffer=new char[len+1];//Khoi tao chuoi voi do dai+1 de chua ki tu '\0'
	size=gSynchConsole->Read(buffer,len);//Doc chuoi tren man hinh
	buffer[size]='\0';//Them ki tu ket thuc '\0' vao cuoi chuoi
	for(;i<len;i++)
	{
		machine->WriteMem(virtAddr+i,1,buffer[i]); //Copy vung nho tu Systemspace vao Userspace
	}
	delete[] buffer;
	return;
}

void EH_PrintString()
{
	int virtAddr,len=0;
	int oneChar=0;
	int i=0;
	char *buffer;
	virtAddr=machine->ReadRegister(4);//Doc vi tri cua chuoi
	do{//Dem do dai cua chuoi
	machine->ReadMem(virtAddr+len,1,&oneChar);
	if(oneChar=='\0')
		break;
	len++;
	}while(1);
	buffer=new char [len];
	for(;i<len;i++)
	{
		machine->ReadMem(virtAddr+i,1,&oneChar);
		buffer[i]=(unsigned char)oneChar;//Copy vung nho tu Userspace vao Systemspace
	}
	gSynchConsole->Write(buffer,len);//Xuat chuoi ra man hinh
	delete[] buffer;
	return;	
}
void EH_Exec(){
    int virtAddr;
    virtAddr = machine->ReadRegister(4);	// doc dia chi ten chuong trinh tu thanh ghi r4
    char* name;
    name = User2System(virtAddr, MaxFileLength + 1); // Lay ten chuong trinh, nap vao kernel
    // neu bi loi thi gan -1 vao thanh ghi 2
    if(name == NULL)
    {
        DEBUG('a', "\n Not enough memory in System");
        printf("\n Not enough memory in System");
        machine->WriteRegister(2, -1);
        return;
    }
    OpenFile *excecutable = fileSystem->Open(name);
    if (excecutable == NULL)
    {
        printf("\nExec:: Can't open this file.");
        machine->WriteRegister(2,-1);
        return;
    }
    delete excecutable;
    // neu khong loi thi tra ve id cua thread dang chay
    int id = processTab->ExecUpdate(name); 
    machine->WriteRegister(2,id);
    delete[] name;	
}
void EH_Join(){       
    int id = machine->ReadRegister(4);
    int res = processTab->JoinUpdate(id);
    machine->WriteRegister(2, res);
}
void EH_Exit(){
    // avoid harry
    IntStatus oldLevel = interrupt->SetLevel(IntOff);

    int exitStatus;
    exitStatus = machine->ReadRegister(4);

    // if process exited with error, print error
    if (exitStatus != 0)
        printf("\nProcess %s exited with error level %d",currentThread->getName(),exitStatus);

    (void) interrupt->SetLevel(oldLevel);
    interrupt->Halt();
}

void
ExceptionHandler(ExceptionType which)
{
    int type = machine->ReadRegister(2);

    // if ((which == SyscallException) && (type == SC_Halt)) {
	// DEBUG('a', "Shutdown, initiated by user program.\n");
   	// interrupt->Halt();
    // } else {
	// printf("Unexpected user mode exception %d %d\n", which, type);
	// ASSERT(FALSE);
    // }

    switch(which){
        //Xu li cac exception
        case NoException:
            return;

        case PageFaultException:
            printf("Page Fault Exception.\n");
            ASSERT(FALSE);
            break;
        
        case ReadOnlyException:
            printf("Read Only Exception.\n");
            ASSERT(FALSE);
            break;
        
        case BusErrorException:
            printf("Bus Error Exception.\n");
            ASSERT(FALSE);
            break;
        
        case AddressErrorException:
            printf("Address Error Exception.\n");
            ASSERT(FALSE);
            break;
        
        case OverflowException:
            printf("Overflow Exception.\n");
            ASSERT(FALSE);
            break;
        
        case IllegalInstrException:
            printf("Illegal Instr Exception.\n");
            ASSERT(FALSE);
            break;
        
        case NumExceptionTypes:
            printf("Num Exception Types.\n");
            ASSERT(FALSE);
            break;

        case SyscallException:{
            switch(type){
                //Xu li cac system call
                case SC_Halt:
                    DEBUG('a',"Shutdown, initiated by user program.\n");
                    interrupt->Halt();
                    break;
                case SC_ReadInt:
                    EH_ReadInt();
                    IncProgCounter();
                    break;
                
                case SC_PrintInt:
                    EH_PrintInt();
                    IncProgCounter();
                    break;

                case SC_ReadChar:
                    EH_ReadChar();
                    IncProgCounter();
                    break;

                case SC_PrintChar:
                    EH_PrintChar();
                    IncProgCounter();
                    break;

                case SC_ReadString:
                    EH_ReadString();
                    IncProgCounter();
                    break;

                case SC_PrintString:
                    EH_PrintString();
                    IncProgCounter();
                    break;
                case SC_Exec:
                    EH_Exec();
                    IncProgCounter();
                    break;
                case SC_Join:
                    EH_Join();
                    IncProgCounter();
                    break;
                case SC_Exit:
                    EH_Exit();
                    IncProgCounter();
                    break;
                default:
                    IncProgCounter();
            }
            break;
        }
    }
}
