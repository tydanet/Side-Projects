#include "fs.h"

// highly optimized, nearly unreadable
int find_open_bit()
{
    for(int i = 0; i < NUM_BLOCKS/8; i++)
    {
        if((255-bitvector[i])%256 > 0)
        {
            printf("Found open bit at %d\n",8*i+(int)log2(256-(255-bitvector[i])));
            return 8*i+(int)log2(256-((255-bitvector[i])%256));
        }
    }
    printf("No open bit found.\n");
    return -1;
}

// not completely done yet
void flip_bit(int idx)
{
    bitvector[idx / 8] = (int) bitvector[idx / 8] ^ (int) pow(2, idx % 8);
}

int find_file(char *name)
{
    int stack[NUM_BLOCKS];
    int stack_pointer = 0;

    // start search from root directory
    stack[0] = 0;

    int size, mem_index;

    while(stack_pointer >= 0)
    {
        // pop top-most element of the stack
        mem_index = stack[stack_pointer];
        stack_pointer--;
        
        if(strcmp(memory[mem_index].content.fd.name, name) == 0)
        {
            printf("Found %s at %d.\n", name, mem_index);
            return mem_index;
        }
        if(memory[mem_index].type == DIR_T)
        {
            int index_index;
            size = memory[mem_index].content.fd.size;

            for(int i = 0; i < size; i++)
            {
                // push file descriptor locationss on the stack
                stack_pointer++;
                index_index = memory[mem_index].content.fd.block_ref;
                stack[stack_pointer] = memory[index_index].content.index[i];
            }
        }
    }
    printf("%s not found.\n", name);
    return -1;
}

void create_file(char *name, int type, char *dir)
{
    printf("Creating %s in directory %s.\n", name, dir);
    // location of the descriptor and the data
    int fd_index, data_index, dir_index, index_index;

    // find next open block for file descriptor and mark it as occupied
    fd_index = find_open_bit();
    flip_bit(fd_index);

    // do the same for where data is to be stored
    data_index = find_open_bit();
    flip_bit(data_index);

    printf("Reserving %d and %d for %s.\n", fd_index, data_index, name);

    // root folder has no parent, so skip over this 
    if(strcmp(name, "/") != 0)
    {
        // find index of directory file resides in
        dir_index = find_file(dir);
        index_index = memory[dir_index].content.fd.block_ref;

        // set index block at index of current directory size to file descriptor's index and increment size
        memory[index_index].content.index[memory[dir_index].content.fd.size] = fd_index;
        memory[dir_index].content.fd.size++;

        memory[fd_index].content.fd.parent_ref = dir_index;
    }

    // set types
    memory[fd_index].type = type;

    if(type == FILE_T)
        memory[data_index].type = DATA;

    else if(type == DIR_T)
        memory[data_index].type = INDEX;

    // set file name
    strcpy(memory[fd_index].content.fd.name, name);
    //printf("Creating %s in directory %s.\n", memory[fd_index].content.fd.name, dir);

    // set reference to data
    memory[fd_index].content.fd.block_ref = data_index;
    //printf("Setting block reference to %d.\n", memory[fd_index].content.fd.block_ref);
}

void delete_file(char *name)
{
    int loc = find_file(name);
    
    if(memory[loc].type == DIR_T)
    {
        int size = memory[loc].content.fd.size;
        int index_loc = memory[loc].content.fd.block_ref;

        for(int i = 0; i < size; i++)
        {
            delete_file(memory[memory[index_loc].content.index[i]].content.fd.name);
            //memory[loc].content.fd.size--;
        }
        printf("Deleting %s.\n", memory[loc].content.fd.name);

        flip_bit(index_loc);
        flip_bit(loc);

        memory[memory[loc].content.fd.parent_ref].content.fd.size--;
    }
    else if(memory[loc].type == FILE_T)
    {
        int data_loc = memory[loc].content.fd.block_ref;
        printf("Deleting %s.\n", memory[loc].content.fd.name);

        flip_bit(data_loc);
        flip_bit(loc);
    }
}

void init()
{
    printf("Allocating %d bytes to memory.\n", NUM_BLOCKS * BLOCK_SIZE);
    memory = calloc(NUM_BLOCKS, BLOCK_SIZE);

    printf("Allocating %d bytes to bit vector.\n", NUM_BLOCKS);
    bitvector = calloc(NUM_BLOCKS, sizeof(char));

    printf("Creating Superblock\n");
    create_file("/", DIR_T, NULL);
}

void display_bits()
{
    printf("Bit vector: %s", bitvector);

    printf("\n\n");
}

//void reindex(NODE *descriptor, int index)
//{
//    int arr[descriptor.content.fd.size];
//
//    for(int i = 0; i < descriptor.content.fd.size; i++)
//    {
//    }
//}

int main()
{
    init();

    create_file("DIR_A", DIR_T, "/");
    create_file("DIR_B", DIR_T, "DIR_A");
    
    create_file("a", FILE_T, "DIR_A");
    create_file("b", FILE_T, "DIR_B");
    
    create_file("b1", FILE_T, "DIR_B");
    create_file("a1", FILE_T, "DIR_A");
    create_file("c", FILE_T, "/");

    delete_file("DIR_A");

    create_file("d", FILE_T, "/");

    find_file("a1");
    find_file("a2");

    free(memory);
    free(bitvector);

    return 0;
}
