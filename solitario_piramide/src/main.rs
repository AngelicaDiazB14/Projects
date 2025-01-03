

use rand::seq::SliceRandom;
use rand::SeedableRng;
use rand::rngs::StdRng;
use std::collections::HashMap;
use std::fs::OpenOptions;
use std::io::{self, Write};
use crossterm::event::{self, Event, KeyCode};

fn representar_carta(valor: u8) -> String {
    match valor {
        1 => "A".to_string(),
        10 => "Z".to_string(),
        11 => "J".to_string(),
        12 => "Q".to_string(),
        13 => "K".to_string(),
        _ => valor.to_string(),
    }
}

fn crear_baraja(semilla: Option<u64>) -> Vec<(u8, char, char)> {
    let palos = vec!['C', 'E', 'T', 'D'];  // Corazones, Espadas, Tréboles, Diamantes
    let colores = [('C', 'r'), ('E', 'n'), ('T', 'n'), ('D', 'r')].iter().cloned().collect::<HashMap<_, _>>();
    let mut baraja = Vec::new();

    for &palo in &palos {
        for valor in 1..=13 {
            baraja.push((valor, palo, *colores.get(&palo).unwrap()));
        }
    }

    // Inicializar el generador de números aleatorios con la semilla proporcionada
    let mut rng: StdRng = match semilla {
        Some(s) => SeedableRng::seed_from_u64(s),
        None => SeedableRng::from_entropy(),
    };
    baraja.shuffle(&mut rng);
    baraja
}


fn crear_piramide(baraja: &[(u8, char, char)]) -> (Vec<Vec<(u8, char, char)>>, Vec<(u8, char, char)>) {
    let mut piramide = Vec::new();
    let mut indice = 0;

    for i in 1..8 {
        let mut fila = Vec::new();
        for _ in 0..i {
            fila.push(baraja[indice]);
            indice += 1;
        }
        piramide.push(fila);
    }

    let mazo = baraja[indice..].to_vec();
    (piramide, mazo)
}

fn mostrar_piramide(piramide: &[Vec<(u8, char, char)>], mazo: &[(u8, char, char)], carta_volteada: Option<(u8, char, char)>, puntaje: u32) {
    // Limpiar la pantalla antes de mostrar la pirámide
    print!("\x1B[2J\x1B[1;1H");
    io::stdout().flush().unwrap();

    // Mostrar puntaje
    println!("Puntaje: {}", puntaje);

    // Calcular el ancho total de la pirámide
    let piramide_width = piramide.last().unwrap().len() * 3 + piramide.len() - 1;

    // Mostrar la pirámide
    for (i, fila) in piramide.iter().enumerate() {
        let mut salida = String::new();
        // Agregar espacios en blanco para alinear a la derecha
        for _ in 0..(piramide_width - i * 2 - 1) {
            salida.push(' ');
        }
        // Agregar las cartas de la fila
        for carta in fila.iter() {
            salida.push_str(&format!("{}{}{} ", representar_carta(carta.0), carta.1, carta.2));
        }
        println!("{}", salida);
    }

    // Mostrar las cartas del mazo
    if !mazo.is_empty() {
        println!("\nCartas de reserva: {}\n", "XXX ".repeat(mazo.len()).trim_end());
    } else {
        println!("\nPresione Enter para usar las cartas desechadas.\n");
    }

    // Mostrar la carta volteada si existe
    if let Some(carta) = carta_volteada {
        println!("Carta volteada del mazo: {}{}{}", representar_carta(carta.0), carta.1, carta.2);
    }
}


fn guardar_estado(piramide: &[Vec<(u8, char, char)>], mazo: &[(u8, char, char)], carta_volteada: Option<(u8, char, char)>, puntaje: u32, accion: &str) {
    let mut archivo = OpenOptions::new().append(true).create(true).open("log.txt").unwrap();
    writeln!(archivo, "Acción: {}", accion).unwrap();
    writeln!(archivo, "Puntaje: {}", puntaje).unwrap();
    
    // Guardar la pirámide
    for fila in piramide {
        let salida: String = fila.iter().map(|carta| format!("{}{}{}", representar_carta(carta.0), carta.1, carta.2)).collect::<Vec<_>>().join(" ");
        writeln!(archivo, "{}", salida).unwrap();
    }

    // Guardar las cartas del mazo
    if !mazo.is_empty() {
        let mazo_salida: String = mazo.iter().map(|carta| format!("{}{}{}", representar_carta(carta.0), carta.1, carta.2)).collect::<Vec<_>>().join(" ");
        writeln!(archivo, "\nCartas de reserva: {}\n", mazo_salida).unwrap();
    } else {
        writeln!(archivo, "\nNo hay más cartas en la reserva.\n").unwrap();
    }

    // Guardar la carta volteada si existe
    if let Some(carta) = carta_volteada {
        writeln!(archivo, "Carta volteada del mazo: {}{}{}", representar_carta(carta.0), carta.1, carta.2).unwrap();
    }
}

fn carta_descubierta(piramide: &[Vec<(u8, char, char)>], fila: usize, columna: usize) -> bool {
    let mut cartas_restantes = 0;
    for fila in piramide.iter() {
        for carta in fila {
            if carta.0 != 0 {
                cartas_restantes += 1;
            }
        }
    }

    if cartas_restantes <= 2 {
        return true;
    }

    if fila == piramide.len() - 1 {
        return true; // Las cartas en la fila inferior siempre están descubiertas
    }

    if fila + 1 < piramide.len() {
        let fila_inferior = &piramide[fila + 1];
        if columna < fila_inferior.len() && fila_inferior[columna].0 != 0 {
            return false; // La carta está cubierta por la carta abajo a la izquierda
        }
        if columna + 1 < fila_inferior.len() && fila_inferior[columna + 1].0 != 0 {
            return false; // La carta está cubierta por la carta abajo a la derecha
        }
    }

    true // La carta no está cubierta
}




fn eliminar_carta(piramide: &mut Vec<Vec<(u8, char, char)>>, fila: usize, columna: usize) {
    piramide[fila][columna] = (0, ' ', ' ');
}


fn intentar_emparejar_con_volteada(piramide: &mut Vec<Vec<(u8, char, char)>>, carta_volteada: (u8, char, char), columna: usize, puntaje: &mut u32) -> bool {
    let mut fila = piramide.len() - 1;
    let columna = columna - 1;  // Ajustar a índice base 0

    while fila > 0 && piramide[fila][columna].0 == 0 {
        fila -= 1;
    }

    if piramide[fila][columna].0 + carta_volteada.0 != 13 {
        return false;
    }

    let es_descubierta = carta_descubierta(piramide, fila, columna) || fila == piramide.len() - 1;
    if es_descubierta {
        eliminar_carta(piramide, fila, columna);
        *puntaje += 2;
        true
    } else {
        false
    }
}



fn intentar_eliminar_pareja(piramide: &mut Vec<Vec<(u8, char, char)>>, fila1: usize, col1: usize, fila2: usize, col2: usize, puntaje: &mut u32) -> bool {
    if piramide[fila1][col1].0 + piramide[fila2][col2].0 == 13 {
        if carta_descubierta(piramide, fila1, col1) && carta_descubierta(piramide, fila2, col2) {
            eliminar_carta(piramide, fila1, col1);
            eliminar_carta(piramide, fila2, col2);
            *puntaje += 2;
            return true;
        }
    }
    false
}

fn intentar_eliminar_rey(piramide: &mut Vec<Vec<(u8, char, char)>>, col: usize, puntaje: &mut u32) -> bool {
    let mut fila = piramide.len() - 1;
    let col = col - 1; // Ajustar a índice base 0

    while fila > 0 && piramide[fila][col].0 == 0 {
        fila -= 1;
    }

    if piramide[fila][col].0 != 13 {
        return false;
    }

    if carta_descubierta(piramide, fila, col) {
        eliminar_carta(piramide, fila, col);
        *puntaje += 1;
        return true;
    } else {
        false
    }
}




fn eliminar_filas_vacias(piramide: &mut Vec<Vec<(u8, char, char)>>) {
    piramide.retain(|fila| fila.iter().any(|carta| carta.0 != 0));
}



fn voltear_mazo(mazo: &mut Vec<(u8, char, char)>, descartadas: &mut Vec<(u8, char, char)>, reutilizado: &mut bool) -> Option<(u8, char, char)> {
    if !mazo.is_empty() {
        Some(mazo.remove(0))
    } else if !*reutilizado && !descartadas.is_empty() {
        // Reutilizar las cartas desechadas una vez
        mazo.append(descartadas);
        let mut rng = StdRng::from_entropy();
        mazo.shuffle(&mut rng);
        *reutilizado = true;
        Some(mazo.remove(0))
    } else {
        None
    }
}


fn verificar_condicion_derrota(piramide: &[Vec<(u8, char, char)>], mazo: &[(u8, char, char)], reutilizado: bool) -> (bool, u32) {
    // Verificar si hay movimientos posibles en la pirámide
    for fila in 0..piramide.len() {
        for col in 0..piramide[fila].len() {
            if piramide[fila][col].0 == 0 {
                continue;
            }

            // Verificar emparejamientos con cartas adyacentes
            for (fila2, col2) in &[(fila + 1, col), (fila + 1, col + 1)] {
                if *fila2 < piramide.len() && *col2 < piramide[*fila2].len() && piramide[*fila2][*col2].0 != 0 {
                    if piramide[fila][col].0 + piramide[*fila2][*col2].0 == 13 {
                        return (false, 0); // Hay un movimiento posible
                    }
                }
            }

            // Verificar si la carta es un rey
            if piramide[fila][col].0 == 13 {
                return (false, 0); // Hay un movimiento posible
            }
        }
    }

    // Verificar si hay movimientos posibles con la carta volteada
    if !mazo.is_empty() || !reutilizado {
        return (false, 0); // Aún quedan cartas por voltear
    }

    // Verificar si se ha ganado
    if piramide.iter().all(|fila| fila.iter().all(|carta| carta.0 == 0)) {
        return (true, 38); // Ganó con un puntaje de 38
    }

    // No hay movimientos posibles
    (true, 0) // Perdió
}



fn jugar_nuevamente() -> bool {
    let mut respuesta = String::new();
    loop {
        println!("¿Desea jugar nuevamente? (s/n): ");
        io::stdin().read_line(&mut respuesta).unwrap();
        respuesta = respuesta.trim().to_lowercase().to_string(); // Convertir la respuesta a minúsculas y quitar espacios en blanco al inicio y al final
        match respuesta.as_str() {
            "s" | "si" | "sí" => return true,
            "n" | "no" => return false,
            _ => println!("Respuesta no válida. Por favor, responda con 's' o 'n'."),
        }
        respuesta.clear();

        // Limpiar el buffer de entrada
        let mut buffer = String::new();
        io::stdin().read_line(&mut buffer).unwrap();
    }
}


#[derive(Clone)]
struct EstadoJuego {
    piramide: Vec<Vec<(u8, char, char)>>,
    mazo: Vec<(u8, char, char)>,
    carta_volteada: Option<(u8, char, char)>,
    puntaje: u32,
}

fn jugar_pyramid(semilla: Option<u64>) {
    let mut nuevo_juego = true;  // Variable para controlar si se inicia un nuevo juego

    loop {
        if nuevo_juego {
            let mut baraja = crear_baraja(semilla);
            let (mut piramide, mut mazo) = crear_piramide(&baraja);
            let mut carta_volteada: Option<(u8, char, char)> = None;
            let mut puntaje = 0;
            let mut historial: Vec<EstadoJuego> = Vec::new();
            let mut descartadas: Vec<(u8, char, char)> = Vec::new();  // Cartas desechadas
            let mut reutilizado = false;  // Bandera para indicar si las cartas desechadas ya se han reutilizado

            nuevo_juego = false;  // Se establece a false para evitar crear una nueva baraja repetidamente

            loop {
                mostrar_piramide(&piramide, &mazo, carta_volteada, puntaje);

                if let Some(carta) = carta_volteada {
                    if carta.0 == 13 {
                        println!("Se elimina el rey automáticamente.");
                        carta_volteada = None;
                    } else {
                        println!("===========================================================");
                        println!("=                 Acciones disponibles                    =");
                        println!("=                                                         =");
                        println!("= 1. Emparejar con carta de la pirámide                   =");
                        println!("= 2. Descartar carta                                      =");
                        println!("===========================================================");
                        let mut accion = String::new();
                        io::stdin().read_line(&mut accion).unwrap();
                        guardar_estado(&piramide, &mazo, carta_volteada, puntaje, &accion);
                        match accion.trim() {
                            "2" => {
                                descartadas.push(carta_volteada.unwrap());  // Agregar la carta volteada a las desechadas
                                carta_volteada = None;
                            },
                            "1" => {
                                let mut columna = String::new();
                                println!("Columna de la carta de la pirámide (1 a 7): ");
                                io::stdin().read_line(&mut columna).unwrap();
                                let columna: usize = match columna.trim().parse() {
                                    Ok(num) if num >= 1 && num <= 7 => num,
                                    _ => {
                                        println!("Entrada no válida. Volviendo al menú.");
                                        continue;
                                    }
                                };

                                if intentar_emparejar_con_volteada(&mut piramide, carta, columna, &mut puntaje) {
                                    eliminar_filas_vacias(&mut piramide);
                                } else {
                                    println!("Movimiento no válido.");
                                }
                                carta_volteada = None;
                        }
                            _ => println!("Acción no reconocida."),
                        }
                    }
                } else {
                    println!("===========================================================");
                    println!("=                 Acciones disponibles                    =");
                    println!("=                                                         =");
                    println!("= 1. Emparejar cartas de la pirámide                      =");
                    println!("= 2. Eliminar rey                                         =");
                    println!("= 3. Sacar de la reserva (<ENTER>)                        =");
                    println!("= 4. Juego nuevo (N/n)                                    =");
                    println!("= 5. Salir (ESC)                                          =");
                    println!("===========================================================");

                    if let Event::Key(key_event) = event::read().unwrap() {
                        let accion = match key_event.code {
                            KeyCode::Esc => "5".to_string(),
                            KeyCode::Char('5') => "5".to_string(),
                            KeyCode::Char('4') | KeyCode::Char('n') | KeyCode::Char('N') => "4".to_string(),
                            KeyCode::Char('3') => "".to_string(),
                            KeyCode::Enter => "".to_string(),
                            KeyCode::Char('2') => "2".to_string(),
                            KeyCode::Char('1') => "1".to_string(),
                            KeyCode::Char('u') | KeyCode::Char('U') => "6".to_string(),
                            _ => continue,
                        };

                        guardar_estado(&piramide, &mazo, carta_volteada, puntaje, &accion);

                        match accion.trim().to_lowercase().as_str() {
                            "5" => {
                                println!("Saliendo del juego...");
                                std::process::exit(0);
                            }
                            "4" => {
                                nuevo_juego = true;  // Se indica iniciar un nuevo juego
                                break;
                            }
                            "" | "3" => {
                                carta_volteada = voltear_mazo(&mut mazo, &mut descartadas, &mut reutilizado);
                                if carta_volteada.is_none() {
                                    println!("El mazo está vacío.");
                                }
                            }
                            "2" => {
                                let mut columna = String::new();
                                println!("Columna de la carta a eliminar (1 a 7): ");
                                io::stdin().read_line(&mut columna).unwrap();
                                let columna: usize = match columna.trim().parse() {
                                    Ok(num) if num >= 1 && num <= 7 => num,
                                    _ => {
                                        println!("Entrada no válida. Volviendo al menú.");
                                        continue;
                                    }
                                };
                                if intentar_eliminar_rey(&mut piramide, columna, &mut puntaje) {
                                    eliminar_filas_vacias(&mut piramide);
                                } else {
                                    println!("Movimiento no válido.");
                                }
                            }
                            "1" => {
                                let mut columna1 = String::new();
                                println!("Columna de la primera carta (1 a 7): ");
                                io::stdin().read_line(&mut columna1).unwrap();
                                let columna1: usize = match columna1.trim().parse() {
                                    Ok(num) if num >= 1 && num <= 7 => num,
                                    _ => {
                                        println!("Entrada no válida. Volviendo al menú.");
                                        continue;
                                    }
                                };

                                let mut fila1 = piramide.len() - 1;
                                while fila1 > 0 && piramide[fila1][columna1 - 1].0 == 0 {
                                    fila1 -= 1;
                                }

                                let mut columna2 = String::new();
                                println!("Columna de la segunda carta (1 a 7): ");
                                io::stdin().read_line(&mut columna2).unwrap();
                                let columna2: usize = match columna2.trim().parse() {
                                    Ok(num) if num >= 1 && num <= 7 => num,
                                    _ => {
                                        println!("Entrada no válida. Volviendo al menú.");
                                        continue;
                                    }
                                };

                                let mut fila2 = piramide.len() - 1;
                                while fila2 > 0 && piramide[fila2][columna2 - 1].0 == 0 {
                                    fila2 -= 1;
                                }
                                if fila1 > 0 && fila2 > 0 && intentar_eliminar_pareja(&mut piramide, fila1, columna1 - 1, fila2, columna2 - 1, &mut puntaje) {
                                    eliminar_filas_vacias(&mut piramide);
                                } else {
                                    println!("Movimiento no válido.");
                                }
                            }
                           "6" => {
                            if let Some(estado_anterior) = historial.pop() {
                                piramide = estado_anterior.piramide;
                                mazo = estado_anterior.mazo;
                                carta_volteada = estado_anterior.carta_volteada;
                                puntaje = estado_anterior.puntaje;
                                reutilizado = false;  // Restablecer la bandera de reutilización
                            } else {
                                println!("No hay movimientos para deshacer.");
                            }
                            }
                            _ => println!("Acción no reconocida."),
                        }
                    }
                }

                let (condicion, puntaje) = verificar_condicion_derrota(&piramide, &mazo, reutilizado);
                if condicion {
                    if puntaje > 0 {
                        println!("¡Has ganado con un puntaje de {}!", puntaje);
                    } else {
                        println!("No hay más movimientos posibles. Has perdido.");
                    }
                    break;
                }

                // Guarda el estado actual antes de continuar
                let ultimo_estado = Some(EstadoJuego {
                    piramide: piramide.clone(),
                    mazo: mazo.clone(),
                    carta_volteada,
                    puntaje,
                });

                historial.push(ultimo_estado.unwrap());
            }
        }

        if !jugar_nuevamente() {
            break;
        }
    }
}

fn main() {
    let mut args = std::env::args().skip(1);
    let semilla: Option<u64> = args.next().and_then(|s| s.parse().ok());

    jugar_pyramid(semilla);
}