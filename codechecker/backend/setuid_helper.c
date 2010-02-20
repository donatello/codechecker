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

    //TODO: place submission in a chroot jail.
    
    setuid(1002);    
    struct rlimit fork_lim ;
    // set limit on number of forks possible.
    fork_lim.rlim_cur = fork_lim.rlim_max = 0; 
    int ret = setrlimit(RLIMIT_NPROC, &fork_lim);
    
    //set limit on the number of files that can be opened.
    fork_lim.rlim_cur = fork_lim.rlim_max = 3;
    ret = setrlimit(RLIMIT_NOFILE, &fork_lim);

    //		printf("ret = %d\n", ret);
    ret = execvp(argv[1], NULL);    
    //		printf("execvp ret = %d\n", ret);

  }
  int status;
  wait(&status);
  if (WIFSIGNALED(status)) {
    return status;
  }
  return 0;
}
