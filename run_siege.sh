#!/bin/bash

siege --concurrent=25 --time=10S "http://localhost:8000/submit"
