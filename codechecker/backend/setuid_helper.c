/* Setuid Helper - ARCH notes
The Code Checker process runs as a non-root user (checker). To run the submission 
programs as a different user than 'checker', we use setuid_helper.c to achieve it.
setuid_helper is a setuid root executable which limits NPROC and NOFILE for itself, so that 
all its child process can inherit the same and changes the user id of the submission. 

Soon it will also run the submission program in a chroot jail preventing it from browsing 
the filesystem.
*/

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
    //ret = setrlimit(RLIMIT_NOFILE, &fork_lim);

    //		printf("ret = %d\n", ret);
    ret = execvp(argv[2], NULL);    
    //arbitrarily chosen to let parent know that execvp failed; we reach here only if execvp fails 
    return 111;
  }
  int status;
  FILE *fp = fopen("/tmp/setuid-helper.debug", "a");
  wait(&status);
  if (WIFSIGNALED(status)) {
   	if(argv[1][0] == '1') fprintf(fp, "submission %s signalled status = %d\n", argv[2], status);
  }
  fclose(fp);
  return status;
}
