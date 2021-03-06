temp = zeros(length(meas), 3);
for i = 1:length(meas)
    if i == 1
        meas_temp = meas;
    else
        meas_temp = [meas(i:end), meas(1:i-1)];
    end
    
    ls = @(M) sum((ref - M.*meas_temp).^2);
    [x, residual] = fmincon(ls, 1, [],[]);
    temp(i, :) = [i, x, residual];
    i
end

%%
[Y, I] = min(temp(:, 3))
i = temp(I, 1);
mag = temp(I, 2);
meas_temp = mag.*[meas(i:end), meas(1:i-1)];
phase = (length(meas) - i)/length(meas) * 360;

plot(ref)
hold on
plot(meas_temp)
title('Least-Squares')
ylabel('Torque (N-m)')
hold off