
from collections import namedtuple

def read_jobs(filename):
    jobs = []
    Job = namedtuple('Job', ['w', 'l'])
    with open(filename) as f:
        n_of_jobs = f.readline()
        for line in f:
            w, l = line.split(' ')
            jobs.append(Job(w=int(w), l=int(l)))
    return jobs

def sort_by_diff(job):
    return (job.w - job.l) * 1000 + job.w

def sort_by_ratio(job):
    return float(job.w)/float(job.l)

def cal_weighted_completion_times(jobs, key_func):
    # sort the jobs by key_func
    sorted_jobs = sorted(jobs, key=key_func, reverse=True)

    # calculate weighted completion time
    cur_time = 0
    tot = 0
    for job in sorted_jobs:
        cur_time += job.l
        tot += job.w * cur_time
    return tot

def main():
    jobs = read_jobs('jobs.txt')

    print cal_weighted_completion_times(jobs, sort_by_diff)
    print cal_weighted_completion_times(jobs, sort_by_ratio)

if __name__ == '__main__':
    main()
