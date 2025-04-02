#!python3
# breadth first recursive multithreaded file search

import argparse
import pathlib
import os, sys, signal
from multiprocessing import Pool
from math import ceil
from time import sleep
from collections import deque
from typing import Generator

DEBUG = False
VOMIT = False

# A simple FIFO wrapper for collections.deque to emulate the queue.Queue interface.
class Queue(deque):
        # Put an item on the "right" side of the deque.
        def put(self, item):
                self.append(item)

        # Get an item from the "left" side of the deque, allowing and ignoring
        # args and kwargs for compatibility with queue.Queue.
        def get(self, *_args, **_kwargs):
                return self.popleft()

        # True if the deque is empty, for compatibility with queue.Queue.
        def empty(self):
                return len(self) == 0

# Output strings to stderr, similar to print()
def error(*strings):
        output = " ".join([str(s) for s in strings])
        sys.stderr.write(f"{output}\n")
        sys.stderr.flush()

# Only output strings if DEBUG or VOMIT are True.
def debug(*strings):
        if not DEBUG and not VOMIT: return
        error(*strings)

# Only output strings if VOMIT is True.
def vomit(*strings):
        if not VOMIT: return
        error(*strings)

# Generates a number of slices of an array equal to slice_count.
def slice_array(ar: list, slice_count: int) -> Generator[list,None,None]:
        wid = ceil(len(ar) / slice_count)
        vomit(f"Slice width: {wid}")

        for idx in range(slice_count):
                pos = idx * wid
                end = min(pos + wid, len(ar))
                vomit(f"yielding slice ar[{pos}:{end}]")
                yield ar[pos:end]

# Initializer for subprocesses to keep them from receiving KeyboardInterrupts.
def worker_init():
        signal.signal(signal.SIGINT, signal.SIG_IGN)

# Check haystack for matches to needles, optionally matching case or whole matches only.
def check_needles(haystack: str, needles: list[str], match_case: bool, whole_match: bool, match_all: bool) -> bool:
        l_haystack = haystack if match_case else haystack.lower()

        needle_found = match_all
        for needle in needles:
                n = needle if match_case else needle.lower()
                if whole_match:
                    if n == l_haystack:
                        if match_all:
                            continue
                        else:
                            needle_found = True
                            break
                elif n in l_haystack:
                        if match_all:
                            continue
                        else:
                            needle_found = True
                            break
                else:
                        if match_all:
                            needle_found = False
                            break
                        else:
                            continue

        return needle_found

# Check for the absolute 'depth' of a path.
def path_depth(p: str) -> int:
        parts = p.split(os.path.sep)

        if len(parts[-1]) == 0:
                return len(parts) - 1
        else:
                return len(parts)


def iterative_search(root: str, needles: list[str], max_depth: int, match_case: bool, whole_match: bool, match_all: bool, match_filenames: bool, starting_paths: list[str]) -> None:
        """
    Perform an iterative, breadth-first search through a directory tree starting from the given root,
    looking for directory names that match any of the provided keywords (needles).

    Parameters:
      root (str): The absolute path to the root directory where the search begins.
      needles (list[str]): A list of keyword strings to search for in directory names.
      max_depth (int): The maximum depth relative to the root to search. A value of 0 means no limit.
      match_case (bool): If True, the matching will be case sensitive.
      whole_match (bool): If True, the directory name must exactly match a keyword; otherwise, substring matching is used.
      match_all (bool): If True, match all needles; otherwise, match any needles.
      match_filenames (bool): If True, match filenames and directories; otherwise, match only directories.
      starting_paths (list[str]): A list of initial directory names (relative to the root) to start searching from.

    Behavior:
      - Immediately prints the full path of any starting directory that matches a keyword.
      - Uses a queue (implemented as a lightweight wrapper around collections.deque) to store directories to explore.
      - Performs a breadth-first traversal of the directory tree.
      - Only descends into directories whose depth relative to the root is less than max_depth.
      - Prints the full path of any directory that matches the search criteria.
    """

    # Determine the depth of the root directory.
        root_depth = path_depth(root)
        
        # Initialize a queue for breadth-first search using starting paths.
        paths = Queue()

        # Enqueue each starting path and print it if the name matches
        for item in starting_paths:
                path = os.path.join(root, item)
                if check_needles(item, needles, match_case, whole_match, match_all):
                    if match_filenames or os.path.isdir(path):
                        print(path)

                # Only add to the queue if we are allowed to traverse deeper.
                if not os.path.isdir(path): continue
                if max_depth != 1:
                        paths.put(path)

        # Process directories until the queue is empty.
        while not paths.empty():
                # Get the next directory to process.
                item = paths.get(False)
                path = os.path.join(root, item)

                try:
                        # List all entries in the current directory.
                        listing = os.listdir(path)
                except KeyboardInterrupt:
                        debug(f"Interrupted by user while attempting to list {path}")
                        sys.exit(1)
                except Exception as ex:
                        debug(f"Encountered exception while attempting to list {path}")
                        print(ex)
                        continue

                # Iterate over each entry in the directory.
                for entry in listing:
                        entry_path = os.path.join(path, entry)
                        # Determine the current depth (for potential debugging or future logic).
                        entry_depth = path_depth(entry_path)
                        
                        try:
                                # Check if the entry is a directory.
                                is_dir = os.path.isdir(entry_path)
                        except KeyboardInterrupt:
                                debug(f"Interrupted by user while attempting to stat {entry_path}")
                                sys.exit(1)
                        except Exception as ex:
                                debug(f"Encountered exception while attempting to stat {entry_path}")
                                raise ex

                        # Check for keyword matches.
                        # Print the path if its name matches
                        if check_needles(entry, needles, match_case, whole_match, match_all):
                            if match_filenames or is_dir:
                                print(entry_path)
                        if is_dir:
                                # Compute the depth relative to the root.
                                depth = path_depth(entry_path) - root_depth
                                # If there's no depth limit or the current depth is within the limit, add to the queue.
                                if max_depth == 0 or (depth < max_depth):
                                        paths.put(entry_path)
                                else:
                                        vomit(f"Not adding {entry_path} to queue because {depth} >= {max_depth}")

                                

def do_search(root_path: str, needles: list[str], max_depth: int, match_case: bool, whole_match: bool, match_all: bool, match_filenames: bool, num_procs: int) -> None:
        """
    Conduct a parallel search for directories containing specified keywords (needles)
    within the directory tree starting at the root_path. The search is distributed
    across multiple subprocesses using a multiprocessing pool.

    Parameters:
      root_path (str): The path to the root directory where the search starts.
      needles (list[str]): A list of keyword strings to search for in directory names.
      max_depth (int): The maximum depth (relative to root_path) to traverse. 
                       A value of 0 indicates no depth limit.
      match_case (bool): If True, performs a case-sensitive match.
      whole_match (bool): If True, directory names must exactly match a needle; otherwise, substring matching is used.
      match_all (bool): If True, match all needles; otherwise, match any needles.
      match_filenames (bool): If True, match filenames and directories; otherwise, match only directories.
      num_procs (int): The number of subprocesses to spawn for parallel processing.

    Behavior:
      - Lists the entries in the root_path directory.
      - Splits the list of directory entries into approximately equal slices for parallel processing.
      - Uses a multiprocessing pool to call the iterative_search function concurrently on each slice.
      - Polls the asynchronous results until all subprocesses have completed.
      - Handles KeyboardInterrupt to allow for graceful termination if the user interrupts the search.
    """

    # List all entries in the root directory.
        dirlist = os.listdir(root_path)
        

        # Divide the directory listing into chunks for parallel processing.
        slices = slice_array(dirlist, num_procs)
        # for i in slices: print(i)

        # Create a multiprocessing pool with the specified number of processes.
        with Pool(num_procs, initializer=worker_init) as pool:
                results = []

                try:
                        # Iterate over each chunk and start a subprocess to handle that chunk.
                        for chunk in slices:
                                # Don't start processes for nothing.
                                if len(chunk) < 1:
                                        vomit(f"Skipping chunk with length {len(chunk)}")
                                        continue
                                vomit(f"Starting process for chunk with length {len(chunk)}")
                                result = pool.apply_async(iterative_search, args=[root_path, needles, max_depth, match_case, whole_match, match_all, match_filenames, chunk])
                                results.append(result)

                        vomit(f"Started {len(results)} subprocesses")
                        all_done = False

                        # Wait until all subprocesses have completed their execution.
                        while not all(result.ready() for result in results):
                                sleep(0.125)

                except KeyboardInterrupt:
                        error("\nInterrupted by user.")
                        pool.terminate()
                except Exception as ex:
                        pool.terminate()
                        error(ex)
                else:
                        pool.close()
                finally:
                        pool.join()

class dummy_parsed():
    # fallback in case the command line option parsing fails for some reason
    # like, perhaps you run from the file explorer
    # instead of the command line
    max_depth = 0
    match_case = False
    whole_match = False
    match_all = True
    match_filenames = True
    procs = os.cpu_count()
    path = os.path.dirname(os.path.realpath(__file__))
    needle = ""


if __name__ == "__main__":
        
        parser = argparse.ArgumentParser(prog="bfsearch", description="Search for keywords in directory names within a given directory tree.")
        parser.add_argument("--max-depth", "-d", type=int, default=0, help="the maximum subfolder depth of the search (default does not limit depth)")
        parser.add_argument("--match-case", "-c", action='store_true', help="match capitalization while searching (default ignores capitalization)")
        parser.add_argument("--whole-match", "-m", action='store_true', help="test for equality with whole words (default finds keywords in substrings)")
        parser.add_argument("--match-all", "-a", action='store_true', help="test for equality with all keywords (default finds any keywords)")
        parser.add_argument("--match-filenames", "-f", action='store_true', help="searches filenames (default finds only folders)")
        parser.add_argument("--procs", "-p", type=int, default=os.cpu_count(), help="specify the number of subprocesses to use (defaults to CPU count)")
        parser.add_argument("path", type=pathlib.Path, help="the root path in which to search")
        parser.add_argument("needle", nargs='+', help='one or more keywords to search for (signify multi-word terms "in quotes")')
        print(parser)
        try:
                parsed_args = parser.parse_args()
                debug(parsed_args)
                interactive_mode = False
        except:
                parsed_args = dummy_parsed()
                print("defaulting to search the current directory ", parsed_args.path)
                parsed_args.needle = input("What are you looking for? ").split(" ")
                interactive_mode = True
        
        error_found = False
        if parsed_args.max_depth < 0:
                error(f"--max-depth must not be negative")
                error_found = True

        if error_found:
                sys.exit(1)
        
        root_path = str(parsed_args.path)
        
        while True:
            if parsed_args.procs > 1 and not DEBUG:
                print(f"Running with {parsed_args.procs} subprocesses.")
                do_search(root_path, parsed_args.needle, parsed_args.max_depth, parsed_args.match_case, parsed_args.whole_match, parsed_args.match_all, parsed_args.match_filenames, parsed_args.procs)
            else:
                if DEBUG: print(f"{parsed_args.procs} subprocesses available, but running single-threaded.")
                iterative_search(root_path, parsed_args.needle, parsed_args.max_depth, parsed_args.match_case, parsed_args.whole_match, parsed_args.match_all, parsed_args.match_filenames, os.listdir(parsed_args.path))
            
            if interactive_mode:
                parsed_args.needle = input("What else are you looking for? ").split(" ")
            else: break
        

