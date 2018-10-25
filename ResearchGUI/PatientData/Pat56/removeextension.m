function [x_finished] = removeextension(x)
    x = strip(x, 'right', 't');
    x = strip(x, 'right', 'x');
    x = strip(x, 'right', 't');
    x_finished = strip(x, 'right', '.');
end

