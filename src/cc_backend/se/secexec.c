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
    

  p = fork();
  if (!p) { 
    freopen(ea.infile, "r", stdin); 
    freopen(ea.outfile, "w", stdout);
    freopen(ea.errfile, "w", stderr);

    /* jailroot is expressed in absolute pathname terms.*/
    
    chdir(ea.jailroot);
    char *curdir = getcwd(NULL, 0);
    ret = chroot(curdir);
    free(curdir);
#ifdef JAIL
    FILE *fp = fopen("./chstuff", "a");
    if(fp) {
      fprintf(fp, "euid = %d ret = %d errno = %d\n", geteuid(), ret, errno);
      fclose(fp);
    }
#endif /* JAIL */
    
    //drop priveleges
    setuid(ea.euid);    

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
#endif /* DBG */
  return status;
}

int main (int argc, char **argv) {
  int c;
  ExecArgs ea;

   while (1) {
        int this_option_optind = optind ? optind : 1;
        int option_index = 0;
        static struct option long_options[] = {
            {"infile", required_argument, 0, 0},
            {"outfile", required_argument, 0, 0},
            {"errfile", required_argument, 0, 0},
            {"jailroot", required_argument, 0, 0},
            {"executable", required_argument, 0, 0},
            {"euid", required_argument, 0, 0},
            {"timelimit", required_argument, 0, 0},
            {"memlimit", required_argument, 0, 0},
            {"maxfilesz", required_argument, 0, 0},
            {0, 0, 0, 0}
        };

       c = getopt_long (argc, argv, "",
                 long_options, &option_index);
        if (c == -1)
            break;

       switch (c) {
        case 0:

#ifdef GETOPT
            printf ("option %s", long_options[option_index].name);
            if (optarg)
                printf (" with arg %s", optarg);
            printf ("\n");
#endif /*GETOPT*/

            switch(option_index) {
              case 0:
                strcpy(ea.infile, optarg);
                break;

              case 1:
                strcpy(ea.outfile, optarg);
                break;

              case 2:
                strcpy(ea.errfile, optarg);
                break;

              case 3:
                strcpy(ea.jailroot, optarg);
                break;

              case 4:
                strcpy(ea.execname, optarg);
                break;

              case 5: 
                ea.euid = atoi(optarg);
                break;

              case 6: 
                ea.timelimit = atoi(optarg);
                break;

              case 7:
                ea.memlimit = atoi(optarg);
                break;

              case 8: 
                ea.maxfilesz = atoi(optarg);
                break;

              default: 
                break;
              
            }
            break;

        }
    } /* option parsing ends */

   int return_status = secure_spawn(ea);

   return return_status;
}
  
