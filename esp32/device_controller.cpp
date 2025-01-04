#include "device_controller.h"
void RunDisplay(void) {
    EPD_init_fast(); //Full screen refresh initialization.
    PIC_display(gImage_1);//To Display one image using full screen refresh.
    EPD_sleep();//Enter the sleep mode and please do not delete it, otherwise it will reduce the lifespan of the screen.
    delay(50000); //Delay for 50s.

    EPD_init(); //Full screen refresh initialization.
    PIC_display_Clear(); //Clear screen function.
    EPD_sleep();//Enter the sleep mode and please do not delete it, otherwise it will reduce the lifespan of the screen.. 
    delay(2000);
    return;
}
