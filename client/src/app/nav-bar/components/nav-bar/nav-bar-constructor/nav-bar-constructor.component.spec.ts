import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NavBarConstructorComponent } from './nav-bar-constructor.component';

describe('NavBarConstructorComponent', () => {
  let component: NavBarConstructorComponent;
  let fixture: ComponentFixture<NavBarConstructorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NavBarConstructorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NavBarConstructorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
