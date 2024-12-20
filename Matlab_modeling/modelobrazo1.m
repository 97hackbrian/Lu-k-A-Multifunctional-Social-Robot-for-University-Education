clc;
clear;
close all;
L1 = 100; 
L2 = 190; 
L3 = 500; 
L4 = 240; 
L(1) = Link('a', L1, 'alpha', pi/2, 'revolute');     %z
L(2) = Link('a', L2, 'alpha', 0, 'revolute');        %  Z
L(3) = Link('a', L3, 'alpha', pi/2, 'revolute');     % X
L(4) = Link('a', L4, 'alpha', 0, 'revolute');        %  Z
robot = SerialLink(L, 'name', 'Lu-k Robotic Arm');


q_init = [0, -pi/6, deg2rad(7.5), 0];

% Menu
while true
    disp('MENU:');
    disp('1. Modo Manual');
    disp('2. Simulación de Movimiento');
    disp('3. Salir');
    choice = input('Seleccione una opción: ');
    
    if choice == 1
        disp('Modo Manual:');
        q1 = deg2rad(input('Ingrese el ángulo para q1 (en grados, máximo ±60°): '));
        q2 = deg2rad(input('Ingrese el ángulo para q2 (en grados, máximo ±60°): '));
        q3 = deg2rad(input('Ingrese el ángulo para q3 (en grados, máximo ±60°): '));
        q4 = deg2rad(input('Ingrese el ángulo para q4 (en grados, máximo ±60°): '));
        
        % Limit angles to ±60° (±pi/3)
        q1 = max(min(q1, pi/3), -pi/3);
        q2 = max(min(q2, pi/3), -pi/3);
        q3 = max(min(q3, pi/3), -pi/3);
        q4 = max(min(q4, pi/3), -pi/3);
        figure;
        robot.teach([q1, q2, q3, q4]);
        title('Modo Manual: Configuración seleccionada');
        
    elseif choice == 2
        
        disp('Simulación de Movimiento:');
        steps = 50; 
        
        
        q1_trajectory = linspace(q_init(1), pi/6, steps); % 30°
        q2_trajectory = linspace(q_init(2), 0, steps);    % 30°
        q3_trajectory = linspace(q_init(3), pi/6, steps); % 30°
        q4_trajectory = linspace(q_init(4), pi/6, steps); % 30°
        
       
        disp('Moviendo q1...');
        for i = 1:steps
            robot.plot([q1_trajectory(i), q_init(2), q_init(3), q_init(4)]);
            pause(0.05);
        end
        pause(1); 
        disp('Moviendo q2...');
        for i = 1:steps
            robot.plot([q1_trajectory(end), q2_trajectory(i), q_init(3), q_init(4)]);
            pause(0.05);
        end
        pause(1);
        
      
        disp('Moviendo q3...');
        for i = 1:steps
            robot.plot([q1_trajectory(end), q2_trajectory(end), q3_trajectory(i), q_init(4)]);
            pause(0.05);
        end
        pause(1);
       
        disp('Moviendo q4...');
        for i = 1:steps
            robot.plot([q1_trajectory(end), q2_trajectory(end), q3_trajectory(end), q4_trajectory(i)]);
            pause(0.05);
        end
        pause(1);
        
        disp('Simulación completada.');
        
    elseif choice == 3
        % Exit
        disp('Saliendo del programa.');
        break;
    else
        disp('Opción inválida. Intente nuevamente.');
    end
end

syms th1 th2 th3 th4 th5 th6 L0 L1 L2 L3 L4 L5
T1 = SCARA.fkine([th1, th2, th3, th4, th5, th6]); % Matriz de transformaci�n