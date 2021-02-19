#include "proflayton.h"
#include "string.h"
#include <hooks.hpp>

u32 overlay = 0;
extern u32 __ovpt_start;
extern u32 __ovpt_end;
u32 loaded_overlays[2] = {0, 0};

void set_overlay_enabled(int ov)
{
    loaded_overlays[ov >> 5] |= 1 << ov;
}

void set_overlay_disabled(int ov)
{
    loaded_overlays[ov >> 5] &= ~(1 << ov);
}

void print_enabled_overlays()
{
    char final[200] = "PDB: Overlays loaded: ";
    char *finalptr = final + sizeof("PDB: Overlays loaded: ");
    char buffer[20];
    for (int ov = 0; ov < 64; ov++)
    {
        if (loaded_overlays[ov >> 5] & (1 << ov))
        {
            sprintf(buffer, "%d ", ov);
            strcpy(finalptr, buffer);
            finalptr += strlen(buffer);
        }
    }
    *finalptr++ = '\n';
    *finalptr++ = 0;
    printf(final);
}

void patchoverlays()
{
    printf("PDB: Loaded Overlay: %d\n", overlay);
    set_overlay_enabled(overlay);
    print_enabled_overlays();
    
    ovpatch_t *ptr = (ovpatch_t *)(&__ovpt_start);
    while (ptr <= (ovpatch_t *) &__ovpt_end)
    {
        if (ptr->overlay == overlay)
        {
            if (ptr->paste_org > 0)
            {
                *((u32*)ptr->paste_org) = *ptr->location;
            }
            *ptr->location = ptr->link ? BL_OPP((u32) ptr->location, (u32) ptr->function_location):
                                          B_OPP((u32) ptr->location, (u32) ptr->function_location);
        }
        ptr++;
    }
}

HOOK(0x0202492c, u32 param1, u32 param2)
{
    overlay = param2;
}

 // FS_LoadOverlay End
 HOOK(0x0202496c)
 {
     patchoverlays();
 }

 // FS_LoadOverlay End
 HOOK(0x0202495c)
 {
      patchoverlays();
 }

 HOOK(0x02024980, u32 param1, u32 param2)
 {
      overlay = param2;
      printf("PDB: Unloaded Overlay %d\n", param2);
      set_overlay_disabled(param2);
      print_enabled_overlays();
 }