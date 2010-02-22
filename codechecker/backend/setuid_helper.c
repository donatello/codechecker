/* 
Setuid Helper - ARCH notes The Code Checker process runs as a non-root
user (checker). To run the submission programs as a different user
than 'checker', we use setuid_helper.c to achieve it.  setuid_helper
is a setuid root executable which limits NPROC and NOFILE for itself,
so that all its child process can inherit the same and changes the
user id of the submission.

This program also places the submission in a hard-coded chroot
jail. This should be owned by the codechecker user and not writable
by the user the submission is going to run as.
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
    //place submission in a chroot jail.
    char jail[] = "/opt/checker/codechecker/backend/submissions/jail/";
    chroot(jail);
    chdir("/");
    
    //drop priveleges
    setuid(1002);    
    struct rlimit lim ;
    // set limit on number of forks possible.
    lim.rlim_cur = lim.rlim_max = 0; 
    int ret = setrlimit(RLIMIT_NPROC, &lim);
    
    //set limit on the number of files that can be opened.
    //lim.rlim_cur = lim.rlim_max = 3;
    //ret = setrlimit(RLIMIT_NOFILE, &lim);

    //		printf("ret = %d\n", ret);
    ret = execvp(argv[2], NULL);    
    //arbitrarily chosen to let parent know that execvp failed; we
    //reach here only if execvp fails
    return 111;
  }
  int status;
  FILE *fp = fopen("/tmp/setuid-helper.debug", "a");
  if(argv[1][0] == '1') 
    fprintf(fp, "submission %s status = %d\n", argv[2], status);
  
  wait(&status);
  if (WIFSIGNALED(status)) {
    if(argv[1][0] == '1') 
      fprintf(fp, "submission %s signalled status = %d\n", argv[2], status);
  }
  fclose(fp);
  return status;
}
