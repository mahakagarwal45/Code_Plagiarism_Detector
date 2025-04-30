def _yield_children(rec):
    # type: (dr.DirectoryRecord) -> Generator
    '''
    An internal function to gather and yield all of the children of a Directory
    Record.

    Parameters:
     rec - The Directory Record to get all of the children from (must be a
           directory)
    Yields:
     Children of this Directory Record.
    Returns:
     Nothing.
    '''
    if not rec.is_dir():
        raise pycdlibexception.PyCdlibInvalidInput('Record is not a directory!')

    last = b''
    for child in rec.children:
        # Check to see if the filename of this child is the same as the
        # last one, and if so, skip the child.  This can happen if we
        # have very large files with more than one directory entry.
        fi = child.file_identifier()
        if fi == last:
            continue

        last = fi
        if child.rock_ridge is not None and child.rock_ridge.child_link_record_exists() and child.rock_ridge.cl_to_moved_dr is not None and child.rock_ridge.cl_to_moved_dr.parent is not None:
            # If this is the case, this is a relocated entry.  We actually
            # want to go find the entry this was relocated to; we do that
            # by following the child_link, then going up to the parent and
            # finding the entry that links to the same one as this one.
            cl_parent = child.rock_ridge.cl_to_moved_dr.parent
            for cl_child in cl_parent.children:
                if cl_child.rock_ridge is not None and cl_child.rock_ridge.name() == child.rock_ridge.name():
                    child = cl_child
                    break
            # If we ended up not finding the right one in the parent of the
            # moved entry, weird, but just return the one we would have
            # anyway.

        yield child