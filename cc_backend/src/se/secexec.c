#include <secexec.h>

struct sigaction alarm_act;
pid_t p;

static void alarm_handler(int signo) 
{
  /* its time to kill the child now! */
  kill(p, SIGKILL);
}

int secure_spawn(ExecArgs ea) {
  int ret;
  char cur_dir[MAX_PATH_LEN], *new_dir = NULL;
  char *targv[2] = {NULL, NULL}; /* dummy second arg for execvp */
    

  // fork argv[1]
  p = fork();
  if (!p) { 
    freopen(ea.infile, "r", stdin); 
    freopen(ea.outfile, "w", stdout);
    freopen(ea.errfile, "w", stderr);

    //change to the jail directory
    
    if(strcmp(ea.jailroot, "")) {
      getcwd(cur_dir, MAX_PATH_LEN);
      new_dir = (char*) malloc(strlen(ea.jailroot)+strlen(cur_dir)+2);
      strcpy(new_dir, cur_dir);
      strcat(new_dir, "/");
      strcat(new_dir, ea.jailroot);
      chdir(new_dir);

      //chroot to the jail directory
      ret = chroot(new_dir);
#ifdef DBG
      FILE *fp = fopen("./chstuff", "a");
      if(fp) {
        fprintf(fp, "errno = %d\n", errno);
        fclose(fp);
      }
#endif
      free(new_dir);
    }
    
    //drop priveleges
    setuid(1002);    

    struct rlimit lim ;
    // set limit on number of forks possible.
    lim.rlim_cur = lim.rlim_max = 0; 
    ret = setrlimit(RLIMIT_NPROC, &lim);

    lim.rlim_cur = lim.rlim_max = ea.memlimit << 20;
    ret = setrlimit(RLIMIT_AS, &lim);

    lim.rlim_cur = ea.timelimit; lim.rlim_max = ea.timelimit + 1;
    ret = setrlimit(RLIMIT_CPU, &lim);

    lim.rlim_cur = lim.rlim_max = ea.maxfilesz << 20;
    ret = setrlimit(RLIMIT_FSIZE, &lim);

    targv[0] = ea.execname;
    ret = execvp(ea.execname, targv); 
    
    //arbitrarily chosen to let parent know that execvp failed; we
    //reach here only if execvp fails
    return 111;
  }

  /* setting up an alarm for 'timelimit+2' seconds, since it includes CPU and I/O time */
  alarm_act.sa_handler = alarm_handler;
  sigaction(SIGALRM, &alarm_act, NULL);
  alarm(ea.timelimit+2); 

  int status;
  struct rusage submission_stats;

  int wait_ret = wait3(&status, 0, &submission_stats);
#ifdef DBG
  FILE *fp = fopen("/tmp/setuid-helper.debug", "a");
  FILE *fs = fopen("/tmp/stats", "w");
    
  if (WIFSIGNALED(status)) {
      fprintf(fp, "submission %s signalled status = %d errno = %d\n", ea.execname, WTERMSIG(status), errno);
    return WTERMSIG(status);
  }
  if (WIFEXITED(status)) {
      fprintf(fp, "child %s exited normally with status = %d errno = %d\n", ea.execname, WEXITSTATUS(status), errno);
    return WEXITSTATUS(status);
  }
    fprintf(fp, "child %s did not exit normally and did not get"
	    " signalled, exited with status = %d errno = %d\n", ea.execname, status, errno);
  fclose(fp);
  fclose(fs);
#endif
  return status;
}
