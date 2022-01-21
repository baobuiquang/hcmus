#include "syscall.h"
int main()
{
	int i;
	char ch;
	PrintString("\n=============== Chuong trinh ascii ===============\n");
	PrintString("----- Bang ma ASCII (ASCII mo rong - 256 ky tu) -----\n");
	PrintString("Decimal -> ASCII Character\n");
	for (i = 0; i < 256; i++) {
		ch = (char)i;
		PrintInt(i);
		PrintString(" -> ");
		PrintChar(ch);
		PrintString("\n");
	}
	PrintString("==================================================\n\n");
	return 0;
}
