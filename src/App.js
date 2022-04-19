/* eslint-disable react/react-in-jsx-scope */
/* eslint-disable react/jsx-key */
import "./App.css";
import { useState } from "react";
import { Recipes } from "./Recipes.js";

function App() {
	const [ingredientList, setIngredientList] = useState([{ ingredient: "" }]);
	const [recipeList, setRecipeList] = useState([]);
	const [getRecipe, setGetRecipe] = useState(false);

	let handleChange = (i, e) => {
		let newFormValues = [...ingredientList];
		newFormValues[i].ingredient = e.target.value;
		setIngredientList(newFormValues);
	};

	let addFormFields = () => {
		setIngredientList([...ingredientList, { ingredient: "" }]);
	};

	let removeFormFields = (i) => {
		let newFormValues = [...ingredientList];
		newFormValues.splice(i, 1);
		setIngredientList(newFormValues);
	};

	let handleBack = () => {
		setGetRecipe(false);
	};

	let handleSubmit = (event) => {
		event.preventDefault();
		let newFormValues = [...ingredientList];
		let ingredientArray = [];
		console.log(newFormValues);
		for (var i = 0; i < newFormValues.length; i++) {
			if (newFormValues[i].ingredient) {
				ingredientArray.push(newFormValues[i].ingredient);
			}
		}
		console.log(ingredientArray);
		let sendJson = {
			ingredients: ingredientArray,
			cuisine: [],
			diet: [],
			intolerances: [],
		};

		// First fetch: sends the ingredient parameters to back-end/API
		fetch("/get_recipes", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(sendJson),
		})
			.then((response) => response.json())
			.then((data) => {
				console.log(data);
				setRecipeList(data);
			});
		setGetRecipe(true);
		alert(JSON.stringify(sendJson));
	};

	const listRecipe = recipeList.map((recipe, i) => (
		<Recipes
			recipe_title={recipe.recipe_title}
			recipe_picture={recipe.recipe_picture}
			recipe_link={recipe.recipe_link}
		/>
	));

	if (getRecipe === false) {
		return (
			// eslint-disable-next-line react/react-in-jsx-scope
			<div className="inputIngredient">
				<div className="container">
					<h2 className="title">
						<span className="title-word title-word-1">Provide </span>
						<span className="title-word title-word-2">your </span>
						<span className="title-word title-word-3">Ingredients </span>
						<span className="title-word title-word-4">here:</span>
					</h2>
				</div>
				<form onSubmit={handleSubmit}>
					{ingredientList.map((element, index) => (
						<div className="form-inline" key={index}>
							<label>{index + 1}.</label>
							<input
								className="searchTerm"
								type="text"
								name="ingredient"
								placeholder="Type in your ingredient..."
								value={element.ingredient || ""}
								onChange={(e) => handleChange(index, e)}
								data-testid="input-ingredient"
							/>
							{index ? (
								<button
									type="button"
									className="buttonRemove"
									onClick={() => removeFormFields(index)}
									data-testid="remove-button"
								>
									<i className="fa fa-trash"></i>
								</button>
							) : null}
						</div>
					))}
					<div>
						<button
							className="buttonAdd"
							type="button"
							onClick={() => addFormFields()}
						>
							<i className="fa fa-plus"></i>
						</button>
						<button className="buttonSubmit" type="submit">
							<i className="fa fa-search"></i>
						</button>
					</div>
				</form>
			</div>
		);
	} else {
		return (
			<div>
				<h1>Recipe Results:</h1>
				<div className="grid-container">
					<ol className="grid-item">{listRecipe}</ol>
				</div>
				<button className="backButton" onClick={() => handleBack()}>Back</button>
			</div>
		);
	}
}

export default App;
