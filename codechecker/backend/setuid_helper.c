/* 
Setuid Helper - ARCH notes The Code Checker process runs as a non-root
user (checker). To run the submission programs as a different user
than 'checker', we use setuid_helper.c to achieve it. It is a setuid root
executable which limits CPU time, memory usage, forks and maximum file size
for its child process. 
*/

#include <errno.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/resource.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <getopt.h>

#define MAX_PATH_LEN 300

struct sigaction alarm_act;
pid_t p;

static void alarm_handler(int signo) 
{
  /* its time to kill the child now! */
  kill(p, SIGKILL);
}

int main(int argc, char* argv[]) {
/* Usage: setuid_helper debug=<bool> timelimit=<secs> memlimit=<MB>
  maxfilesize=<MB> infile=<name> outfile=<name> errfile=<name> testcaseid=<tid> submissionid=<subid> <submission-exec>
  No error checking done, since this will be run only by the Code checker. */
  int c;
  int debug, timelimit, memlimit, maxfilesz, testcaseid, submissionid;
  char infile[MAX_PATH_LEN], outfile[MAX_PATH_LEN], errfile[MAX_PATH_LEN];
  while(1) {
    static struct option long_options[] =
      {
          /* These options set a flag. */
          {"debug",  required_argument, 0, 0},
          {"timelimit",  required_argument, 0, 0},
          {"memlimit",  required_argument, 0, 0},
          {"maxfilesz",  required_argument, 0, 0},
          {"testcaseid",  required_argument, 0, 0},
          {"submissionid",  required_argument, 0, 0},
          {"infile",  required_argument, 0, 0},
          {"outfile",  required_argument, 0, 0},
          {"errfile",  required_argument, 0, 0},
          {0, 0, 0, 0}
      };
    int option_index = 0;
    c = getopt_long (argc, argv, "",
                     long_options, &option_index);
    if(c == -1) 
      break;

    switch (c) {
      case 0:
        switch (option_index) {
          case 0: debug = atoi(optarg);
                  break;

          case 1: timelimit = atoi(optarg);
                  break;

          case 2: memlimit = atoi(optarg);
                  break;

          case 3: maxfilesz = atoi(optarg);
                  break;

          case 4: testcaseid = atoi(optarg);
                  break;

          case 5: submissionid = atoi(optarg);
                  break;

          case 6: strcpy(infile, optarg);
                  break;

          case 7: strcpy(outfile, optarg);
                  break;

          case 8: strcpy(errfile, optarg);
                  break;
        }

       /*   printf("option_index = %d\n", option_index);
        printf ("option %s", long_options[option_index].name);

        if (optarg)
          printf (" with arg %s", optarg);
        printf ("\n");
      */
        break;
      default: 
        abort();
    }
  }
    

  // fork argv[1]
  p = fork();
  if (!p) { 
    freopen(infile, "r", stdin); 
    freopen(outfile, "w", stdout);
    freopen(errfile, "w", stderr);

    //drop priveleges
    //TODO: fetch the uid to run the submission from TestRunner.py
    setuid(1002);    

    struct rlimit lim ;
    // set limit on number of forks possible.
    lim.rlim_cur = lim.rlim_max = 0; 
    int ret = setrlimit(RLIMIT_NPROC, &lim);

    lim.rlim_cur = lim.rlim_max = memlimit << 20;
    ret = setrlimit(RLIMIT_AS, &lim);

    lim.rlim_cur = timelimit; lim.rlim_max = timelimit + 1;
    ret = setrlimit(RLIMIT_CPU, &lim);

    lim.rlim_cur = lim.rlim_max = maxfilesz << 20;
    ret = setrlimit(RLIMIT_FSIZE, &lim);

    ret = execvp(argv[optind], argv+optind);    
    
    //arbitrarily chosen to let parent know that execvp failed; we
    //reach here only if execvp fails
    return 111;
  }

  /* setting up an alarm for 'timelimit+2' seconds, since it includes CPU and I/O time */
  alarm_act.sa_handler = alarm_handler;
  sigaction(SIGALRM, &alarm_act, NULL);
  alarm(timelimit+2); 

  int status;
  struct rusage submission_stats;

  FILE *fp = fopen("/tmp/setuid-helper.debug", "a");
  FILE *fs = fopen("/tmp/stats", "w");
  int wait_ret = wait3(&status, 0, &submission_stats);
  if(wait_ret != -1)
    fprintf(fs, "%d|%d|%lf\n", testcaseid, submissionid, 
        submission_stats.ru_utime.tv_sec + (1e-6) * submission_stats.ru_utime.tv_usec);

  else 
    fprintf(fs, "%d|%d|%d\n", testcaseid, submissionid, -1);
    
  if (WIFSIGNALED(status)) {
    if(debug) 
      fprintf(fp, "submission %s signalled status = %d errno = %d\n", argv[argc-1], WTERMSIG(status), errno);
    return WTERMSIG(status);
  }
  if (WIFEXITED(status)) {
    if(debug) 
      fprintf(fp, "child %s exited normally with status = %d errno = %d\n", argv[argc-1], WEXITSTATUS(status), errno);
    return WEXITSTATUS(status);
  }
  if(debug) 
    fprintf(fp, "child %s did not exit normally and did not get"
	    " signalled, exited with status = %d errno = %d\n", argv[argc-1], status, errno);
  fclose(fp);
  fclose(fs);
  return status;
}
