use std::{io, thread, time::Duration};
use tui::{
    backend::CrosstermBackend, 
    widgets::{Widget, Block, Borders, BorderType},
    layout::{Layout, Constraint, Direction},
    style::{Style, Color},
    Terminal
};

use crossterm::{
    event::{self, DisableMouseCapture, EnableMouseCapture, Event, KeyCode},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};

fn create_block(direction: Borders , title: &str) -> Block<'_> {
    // TODO: pass Style struct as param
    // ref: https://docs.rs/tui/latest/tui/widgets/
    Block::default()
        .title(title)
        .borders(direction)
        .border_style(Style::default().fg(Color::White))
        .border_type(BorderType::Rounded)
        .style(Style::default().bg(Color::Black))
}

fn main() -> Result<(), io::Error> {
    enable_raw_mode()?;
    let mut stdout = io::stdout();
    execute!(stdout, EnterAlternateScreen, EnableMouseCapture)?;
    let backend = CrosstermBackend::new(stdout);
    let mut terminal = Terminal::new(backend)?;

    terminal.draw(|f| {
        let size = f.size();
        let block = create_block(Borders::ALL, "Main");

        /*
            Block::default()
            .title("Block")
            .borders(Borders::ALL);*/
        f.render_widget(block, size);
    })?;

    thread::sleep(Duration::from_millis(5000));

    // restore terminal
    disable_raw_mode()?;
    execute!(
        terminal.backend_mut(),
        LeaveAlternateScreen,
        DisableMouseCapture
    )?;
    terminal.show_cursor()?;

    Ok(())
}
