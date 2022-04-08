import { render, screen, fireEvent } from "@testing-library/react";
import exp from "constants";
import App from "./App";

test("renders page description", () => {
	render(<App />);
	const linkElement = screen.getByText(
		"Please enter your list of ingredients!"
	);
	expect(linkElement).toBeInTheDocument();
});

test("ingredient input renders", () => {
	render(<App />);
	const buttonElement = screen.getByText("Add");
	expect(buttonElement).toBeInTheDocument();

	const inputElement = screen.getByTestId("input-ingredient");
	expect(inputElement).toBeInTheDocument();

	fireEvent.change(inputElement, { target: { value: "eggs" } });

	const newTextElement = screen.getByTestId("input-ingredient");
	expect(newTextElement).toBeInTheDocument("eggs");
});

test("render remove button when more than one ingredient input box", () => {
	render(<App />);
	const buttonElement = screen.getByText("Add");
	expect(buttonElement).toBeInTheDocument();

	fireEvent.click(buttonElement);

	const removeButtonElement = screen.getByTestId("remove-button");
	expect(removeButtonElement).toBeInTheDocument();
});
