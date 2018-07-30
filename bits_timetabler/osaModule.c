#include <Python.h>
#include <stdarg.h>
#include <string.h>
#include <stdlib.h>

int getOSADistance(char* str1,char* str2);
int max(int, ...);
int min(int, ...);

int main(int argc, char **argv)
{
  if(argc<3){ 
    return -1;
  }

  char *str1 = argv[1];
  char *str2 = argv[2];
  return getOSADistance(str1,str2);
}

int getOSADistance(char* str1,char* str2)
{
  int **arr;
  arr = (int**) malloc((strlen(str1)+1)*sizeof(int*));
  for(int i=0;i<strlen(str1)+1;i++){
    arr[i]=(int*) malloc((strlen(str2)+1)*sizeof(int));
    for(int j=0;j<strlen(str2)+1;j++){
      if(i==0||j==0){
	arr[i][j]=max(2,i,j);
      }
      else{
	int cost = 1;
	if(str1[i-1]==str2[j-1])
	  cost = 0;
	arr[i][j] = min(3,arr[i-1][j-1]+cost,arr[i-1][j]+1,arr[i][j-1]+1);
	if(i>1 && j>1 && str1[i-2]==str2[j-1] && str1[i-1]==str2[j-2]){
	  arr[i][j] = min (2,arr[i][j],arr[i-2][j-2]+cost);
	}
      }
    }
  }
  return arr[strlen(str1)][strlen(str2)];
}

int max(int n_args,...){
  int max, a;
  va_list ap;
  va_start(ap, n_args);
  max = va_arg(ap,int);
  for(int i =2;i<=n_args;i++){
    if((a = va_arg(ap,int))>max)     
      max = a;
    
  }
  va_end(ap);
  return max;
}

int min(int n_args,...){
  int min, a;
  va_list ap;

  va_start(ap, n_args);
  min = va_arg(ap,int);
  for(int i =2;i<=n_args;i++){
    if((a = va_arg(ap,int))< min)
      min = a;
  }
  va_end(ap);
  return min;
}



static PyObject* calculateOSADistance(PyObject* self, PyObject* args){
  char *str1, *str2;
  if (!(PyArg_ParseTuple(args,"ss",&str1,&str2)))
    return NULL;
  
  return Py_BuildValue("i",getOSADistance(str1,str2));
}

static PyMethodDef module_methods[] = {{"calcOSADist",calculateOSADistance,METH_VARARGS,"Calculates open string alignment (OSA) a.k.a. Levenstein distance"},
				{NULL,NULL,0,NULL}};

static struct PyModuleDef osaCModule =
  {
   PyModuleDef_HEAD_INIT,
   "osaCModule",
   "C extensions for certain string comparison functions",
   -1,
   module_methods
  };

PyMODINIT_FUNC PyInit_osaCModule(void){
  return PyModule_Create(&osaCModule);
}
