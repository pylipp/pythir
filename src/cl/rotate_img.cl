// simple image rotation

__kernel void rotate_img(
                    /*
                    __read_only image2d_t inImg, 
                    __write_only image2d_t outImg, 
                    sampler_t sampler, */ 
                    __global float* inImg,
                    __global float* outImg,
                    int w, int h,
                    float sinTheta, float cosTheta)
{
    const int ix = get_global_id(0);
    const int iy = get_global_id(1);

    float x0 = 0.5f * w;
    float y0 = 0.5f * h;
    float xoff = ix - x0;
    float yoff = iy - y0;
    int xpos = (int)(xoff*cosTheta + yoff*sinTheta + x0);
    int ypos = (int)(yoff*cosTheta - xoff*sinTheta + y0);

    if ((xpos >= 0) && (xpos < w) && (ypos >= 0) && (ypos < h)) {
        /*
        int2 inCoords, outCoords;
        // switch x and y coordinates
        inCoords.x = ypos, inCoords.y = xpos;
        outCoords.x = ix, outCoords.y = iy;
        float pixel = read_imagef(inImg, sampler, inCoords).x;
        write_imagef(outImg, outCoords, pixel);
        */ 
        outImg[iy*w+ix] = inImg[ypos*w+xpos];
    }
}
