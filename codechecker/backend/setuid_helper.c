#include <sys/types.h>
#include <sys/wait.h>
#include <sys/resource.h>
#include <sys/time.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
  // fork argv[1]
  pid_t p = fork();
  if (!p) { 
    setuid(1002);    
    struct rlimit fork_lim ;
    fork_lim.rlim_cur = fork_lim.rlim_max = 0; 
    int ret = setrlimit(RLIMIT_NPROC, &fork_lim);
    //		printf("ret = %d\n", ret);
    ret = execvp(argv[1], NULL);    
    //		printf("execvp ret = %d\n", ret);

  }
  int status;
  wait(&status);
  if (WIFSIGNALED(status)) {
    return -WTERMSIG(status);
  }
  return 0;
}
