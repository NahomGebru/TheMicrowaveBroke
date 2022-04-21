/* eslint-disable react/react-in-jsx-scope */
/* eslint-disable react/jsx-key */
import "./App.css";
import { useState } from "react";
import { Recipes } from "./Recipes.js";

function App() {
	const cuisineType = ["Asian", "Mexican"];
	const dietType = ["Vegetarian", "Vegan"];
	const allergyType = ["Peanut", "Dairy"];

	const [ingredientList, setIngredientList] = useState([{ ingredient: "" }]); //state for storing ingredients
	const [recipeList, setRecipeList] = useState([]); // state for storing recipe output
	const [getRecipe, setGetRecipe] = useState(false); // state for rendering results page
	const [cuisineList, setCuisineList] = useState(
		new Array(cuisineType.length).fill(false)
	); //state for cuisine filter
	const [allergyList, setAllergyList] = useState(
		new Array(allergyType.length).fill(false)
	); //state for allergy filter
	const [dietList, setDietList] = useState(
		new Array(dietType.length).fill(false)
	); //state for diet filter

	let handleChange = (i, e) => {
		let newFormValues = [...ingredientList];
		newFormValues[i].ingredient = e.target.value;
		setIngredientList(newFormValues);
	};

	// handles cuisine change
	let handleCuisine = (e) => {
		let updatedCheckedState = cuisineList.map((cuisine, index) =>
			index === e ? !cuisine : cuisine
		);
		setCuisineList(updatedCheckedState);
	};

	// handles diet change
	let handleDiet = (e) => {
		let updatedCheckedState = dietList.map((diet, index) =>
			index === e ? !diet : diet
		);
		setDietList(updatedCheckedState);
	};

	// handles allergy change
	let handleAllergy = (e) => {
		let updatedCheckedState = allergyList.map((allergy, index) =>
			index === e ? !allergy : allergy
		);
		setAllergyList(updatedCheckedState);
	};

	// adds new ingredient fields
	let addFormFields = () => {
		setIngredientList([...ingredientList, { ingredient: "" }]);
	};

	// removes ingredient fields
	let removeFormFields = (i) => {
		let newFormValues = [...ingredientList];
		newFormValues.splice(i, 1);
		setIngredientList(newFormValues);
	};

	// handle back button after generating recipe
	let handleBack = () => {
		setGetRecipe(false);
	};

	let handleSave = (recipe) => {
		let sendJson = {
			recipeTitle: recipe.recipe_title,
			imageTitle: recipe.recipe_picture,
			recipeLink: recipe.recipe_link,
		};
		console.log(sendJson);
		fetch("/save_recipes", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(sendJson),
		})
			.then((response) => response.json())
			.then((data) => {
				console.log(data);
			});
		alert("Recipe Saved");
	};

	// handle submit form
	let handleSubmit = (event) => {
		event.preventDefault();

		// Handles ingredients JSON Array
		let newFormValues = [...ingredientList];
		let ingredientArray = [];
		console.log("newFormValues for ingredientList:");
		console.log(newFormValues);
		for (var i = 0; i < newFormValues.length; i++) {
			if (newFormValues[i].ingredient === "") {
				alert("Please enter a ingredient in the empty blanks!");
				return;
			}
			if (newFormValues[i].ingredient) {
				ingredientArray.push(newFormValues[i].ingredient);
			}
		}
		console.log("output of ingredientArray:");
		console.log(ingredientArray);

		// Handles cuisine JSON Array
		newFormValues = [...cuisineList];
		let cuisineArray = [];
		console.log("newFormValues for cuisineList:");
		console.log(newFormValues);
		for (var i = 0; i < newFormValues.length; i++) {
			if (newFormValues[i] == true) {
				cuisineArray.push(cuisineType[i]);
			}
		}
		console.log("output of cuisineArray:");
		console.log(cuisineArray);

		// Handles diet JSON Array
		newFormValues = [...dietList];
		let dietArray = [];
		for (var i = 0; i < newFormValues.length; i++) {
			if (newFormValues[i] == true) {
				dietArray.push(dietType[i]);
			}
		}

		// Handles allergy JSON Array
		newFormValues = [...allergyList];
		let allergyArray = [];
		for (var i = 0; i < newFormValues.length; i++) {
			if (newFormValues[i] == true) {
				allergyArray.push(allergyType[i]);
			}
		}

		// Format Array into JSON Format
		let sendJson = {
			ingredients: ingredientArray,
			cuisine: cuisineArray,
			diet: dietArray,
			intolerances: allergyArray,
		};

		// Sends the parameters to back-end/API
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
	};

	const listRecipe = recipeList.map((recipe, i) => (
		<Recipes
			recipe_title={recipe.recipe_title}
			recipe_picture={recipe.recipe_picture}
			recipe_link={recipe.recipe_link}
			save_recipe={() => handleSave(recipe)}
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
					<div>
						<label>Cuisine: </label>
						<input
							type="checkbox"
							checked={cuisineList[0]}
							onChange={() => handleCuisine(0)}
							name="asian"
							value="asian"
						/>
						<label>Asian | </label>
						<input
							type="checkbox"
							checked={cuisineList[1]}
							onChange={() => handleCuisine(1)}
							name="mexican"
							value="mexican"
						/>
						<label>Mexican </label>
						<br></br>
						<label>Diet: </label>
						<input
							type="checkbox"
							checked={dietList[0]}
							onChange={() => handleDiet(0)}
							name="vegetarian"
							value="vegetarian"
						/>
						<label>Vegetarian | </label>
						<input
							type="checkbox"
							checked={dietList[1]}
							onChange={() => handleDiet(1)}
							name="vegan"
							value="vegan"
						/>
						<label>Vegan </label>
						<br></br>
						<label>Allergies: </label>
						<input
							type="checkbox"
							checked={allergyList[0]}
							onChange={() => handleAllergy(0)}
							name="peanut"
							value="peanut"
						/>
						<label>Peanuts | </label>
						<input
							type="checkbox"
							checked={allergyList[1]}
							onChange={() => handleAllergy(1)}
							name="dairy"
							value="dairy"
						/>
						<label>Dairy </label>
					</div>
					<br></br>
					<label>Ingredients:</label>
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
				<button className="backButton" onClick={() => handleBack()}>
					Back
				</button>
			</div>
		);
	}
}

export default App;
