#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <sys/stat.h>
#include <math.h>

#define NUM_BLOCKS 32
#define BLOCK_SIZE 256
#define MAX_NAME_LENGTH 128
#define DATA_SIZE 254
#define INDEX_SIZE 127

typedef char data_t;
typedef unsigned short index_t;

typedef enum
{
    DIR_T,
    FILE_T,
    INDEX,
    DATA
} NODE_TYPE;

typedef struct fs_node
{
    char name[MAX_NAME_LENGTH];
    time_t create_t;
    time_t access_t;
    time_t mod_t;
    mode_t access;
    unsigned short owner;
    unsigned short size;
    index_t block_ref;
    index_t parent_ref;
} FS_NODE;

typedef struct node
{
    NODE_TYPE type;
    union
    {
        FS_NODE fd;
        data_t data[DATA_SIZE];
        index_t index[INDEX_SIZE];
    } content;
} NODE;

NODE *memory;
char *bitvector;

void init();
void flip_bit(int);
void create_file(char*, int, char*);
void delete_file(char*);
void display_bits();

int find_open_bit();
int find_file(char *);

